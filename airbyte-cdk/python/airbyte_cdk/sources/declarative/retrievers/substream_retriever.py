#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#
from itertools import chain
from typing import Any, Iterable, List, Mapping

from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources.declarative.extractors.http_extractor import HttpExtractor
from airbyte_cdk.sources.declarative.interpolation.interpolated_mapping import InterpolatedMapping
from airbyte_cdk.sources.declarative.requesters.paginators.paginator import Paginator
from airbyte_cdk.sources.declarative.requesters.requester import Requester
from airbyte_cdk.sources.declarative.response import Response
from airbyte_cdk.sources.declarative.retrievers.simple_retriever import SimpleRetriever
from airbyte_cdk.sources.declarative.states.state import State
from airbyte_cdk.sources.declarative.stream_slicers.stream_slicer import StreamSlicer
from airbyte_cdk.sources.streams.core import Stream


class SubstreamRetriever(SimpleRetriever):
    def __init__(
        self,
        name,
        primary_key,
        requester: Requester,
        paginator: Paginator,
        extractor: HttpExtractor,
        stream_slicer: StreamSlicer,
        state: State,
        parent_stream: Stream,
        parent_extractor: HttpExtractor,
        additional_fields: InterpolatedMapping,
    ):
        super().__init__(name, primary_key, requester, paginator, extractor, stream_slicer, state)
        self._parent_stream = parent_stream
        self._parent_extractor = parent_extractor
        self._additional_fields = additional_fields

    def read_records(
        self,
        sync_mode: SyncMode,
        cursor_field: List[str] = None,
        stream_slice: Mapping[str, Any] = None,
        stream_state: Mapping[str, Any] = None,
    ) -> Iterable[Mapping[str, Any]]:
        parent_records = [r for r in self._parent_stream.read_records(SyncMode.full_refresh)]
        for parent_record in parent_records:
            parent_response = Response(body=parent_record)
            # Extract subresource Mapping and create a Response object from it
            sub_response_body = self._parent_extractor.extract_records(parent_response)
            sub_response = Response(body=sub_response_body)

            # Extract records from subresource mapping
            records = self._extractor.extract_records(sub_response)
            next_page_token = self._paginator.next_page_token(sub_response, records)
            if next_page_token:
                # Read records if there are more
                next_pages = super().read_records(sync_mode=SyncMode.full_refresh, stream_slice=stream_slice)
            else:
                next_pages = []
            for record in chain(records, next_pages):
                evaluated_fields = self._additional_fields.eval(
                    config=None, stream_slice=stream_slice, stream_state=stream_state, parent_record=parent_record
                )
                record.update(evaluated_fields)
                yield record