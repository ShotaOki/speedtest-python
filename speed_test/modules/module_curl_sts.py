import json
from modules.module_base import ModuleBase
from modules.type import InputType
from modules.common_boto_as_httprequest import Boto3LowLevelClient


class ModuleCurlSts(ModuleBase):
    @classmethod
    def create_parameter(cls, index: int, input: InputType):

        get_caller_identity = Boto3LowLevelClient("sts").create_request_parameter(
            "GetCallerIdentity", {}
        )

        return {
            "get_caller_identity": ModuleBase.str_with_padding(
                json.dumps(get_caller_identity)
            ),
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        get_caller_identity: str = parameter["get_caller_identity"]
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

        get_caller_identity = json.loads(get_caller_identity.strip())
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        response = urllib3.PoolManager().request(
            method=get_caller_identity["method"],
            url=get_caller_identity["url"],
            body=get_caller_identity["body"],
            headers=get_caller_identity["headers"],
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
        get_caller_identity: str = parameter["get_caller_identity"]
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

        get_caller_identity = json.loads(get_caller_identity.strip())
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
                method=get_caller_identity["method"],
                url=URL(get_caller_identity["url"], encoded=True),
                data=get_caller_identity["body"],
                headers=get_caller_identity["headers"],
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
