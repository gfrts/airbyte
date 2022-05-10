#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#
from typing import List

import pyjq
import requests
from airbyte_cdk.sources.cac.interpolation.eval import JinjaInterpolation
from airbyte_cdk.sources.cac.types import Record


class JqExtractor:
    def __init__(self, transform, vars, config):
        # print(f"creating JqExtractor with transform: {transform}")
        # print(f"creating JqExtractor with config:{config}")
        # print(f"creating JqExtractor with vars:{vars}")
        self._vars = vars
        self._config = config
        self._interpolator = JinjaInterpolation()
        # print("before creating transform")
        self._transform = transform
        # print("after creating transform")

    def extract_records(self, response: requests.Response) -> List[Record]:
        # print(f"extracting records for {response}")
        # print(f"extractor vars: {self._vars}")
        response_body = response.json()
        # print(f"response body: {response_body}")
        # FIXME: need to ensure I'm passing the vars and the parent vars...
        script = self._interpolator.eval(self._transform, self._vars, self._config)
        # print(f"script: {script}")
        return pyjq.all(script, response_body)