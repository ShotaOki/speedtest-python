import json
from modules.module_base import ModuleBase
from modules.type import InputType
from modules.common_boto_as_httprequest import Boto3LowLevelClient


class ModuleCurlBedrock(ModuleBase):
    @classmethod
    def create_parameter(cls, index: int, input: InputType):

        invoke_model = Boto3LowLevelClient(
            "bedrock-runtime", credential_scope="bedrock", region_name="us-east-1"
        ).create_request_parameter(
            "InvokeModel",
            {
                "body": json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 100,
                        "messages": [
                            {
                                "role": "user",
                                "content": "こんにちは、Claude",
                            }
                        ],
                    }
                ),
                "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
                "accept": "application/json",
                "contentType": "application/json",
            },
        )

        return {
            "invoke_model": ModuleBase.str_with_padding(json.dumps(invoke_model)),
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        invoke_model: str = parameter["invoke_model"]
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import json
        import urllib3

        invoke_model = json.loads(invoke_model.strip())
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        response = urllib3.PoolManager().request(
            method=invoke_model["method"],
            url=invoke_model["url"],
            body=invoke_model["body"],
            headers=invoke_model["headers"],
        )
        res = response.data.decode("utf-8")
        # END PROCESS -------------------------

        end_secs = Decimal(perf_counter_ns() - start) / Decimal(10**9)
        print(
            json.dumps(
                {
                    "result": len(res),
                    "elapsed_time": f"{end_secs}",
                    "start_delta": f"{start_delta.total_seconds()}",
                    "processing": processing,
                    "module_name": module_name,
                    "request_id": request_id,
                }
            )
        )

    @classmethod
    async def start_async(cls, parameter):
        invoke_model: str = parameter["invoke_model"]
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import json
        import aiohttp
        from aiohttp.client import URL

        invoke_model = json.loads(invoke_model.strip())
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=invoke_model["method"],
                url=URL(invoke_model["url"], encoded=True),
                data=invoke_model["body"],
                headers=invoke_model["headers"],
            ) as response:
                res = await response.text()
        # END PROCESS -------------------------

        end_secs = Decimal(perf_counter_ns() - start) / Decimal(10**9)
        print(
            json.dumps(
                {
                    "result": len(res),
                    "elapsed_time": f"{end_secs}",
                    "start_delta": f"{start_delta.total_seconds()}",
                    "processing": processing,
                    "module_name": module_name,
                    "request_id": request_id,
                }
            )
        )
