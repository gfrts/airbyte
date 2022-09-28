#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#
import logging
from base64 import b64encode
from typing import Any, List, Mapping, Tuple

import pendulum
from airbyte_cdk import AirbyteLogger
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator

from .api import ActiveUsers, Annotations, AverageSessionLength, Cohorts, Events


class SourceAmplitude(AbstractSource):
    def _convert_auth_to_token(self, username: str, password: str) -> str:
        username = username.encode("latin1")
        password = password.encode("latin1")
        token = b64encode(b":".join((username, password))).strip().decode("ascii")
        return token

    def check_connection(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> Tuple[bool, any]:
        try:
            auth = TokenAuthenticator(token=self._convert_auth_to_token(config["api_key"], config["secret_key"]), auth_method="Basic")
            list(Cohorts(authenticator=auth).read_records(SyncMode.full_refresh))
            return True, None
        except Exception as error:
            return False, f"Unable to connect to Amplitude API with the provided credentials - {repr(error)}"

    @staticmethod
    def _validate_start_date(start_date):
        today = pendulum.now()
        start_date = pendulum.parse(start_date)
        start_date_in_future = start_date > today

        if start_date_in_future:
            logger = logging.getLogger("airbyte")
            logger.info(f"Start date set to {today}.")

            return today.to_datetime_string()
        return start_date

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        config["start_date"] = self._validate_start_date(config.get("start_date"))

        auth = TokenAuthenticator(token=self._convert_auth_to_token(config["api_key"], config["secret_key"]), auth_method="Basic")
        return [
            Cohorts(authenticator=auth),
            Annotations(authenticator=auth),
            Events(authenticator=auth, start_date=config["start_date"]),
            ActiveUsers(authenticator=auth, start_date=config["start_date"]),
            AverageSessionLength(authenticator=auth, start_date=config["start_date"]),
        ]
