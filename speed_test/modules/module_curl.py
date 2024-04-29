from modules.module_base import ModuleBase
from modules.type import InputType


class ModuleCurl(ModuleBase):

    URL_LIST = [
        "https://www.google.com/",
        "https://www.yahoo.co.jp/",
        "https://www.bing.com/",
        "https://www.amazon.co.jp/",
        "https://httpd.apache.org/",
        "https://www.w3.org/",
        "https://www.python.org/",
        "https://www.microsoft.com/",
        "https://www.apple.com/",
        "https://ja.wikipedia.org/",
    ]

    @classmethod
    def create_parameter(cls, index: int, input: InputType):
        return {
            "url": ModuleBase.str_with_padding(cls.URL_LIST[index]),
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        url: str = parameter["url"]
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

        url = url.strip()
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        response = urllib3.PoolManager().request("GET", url)
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
        url: str = parameter["url"]
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

        url = url.strip()
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
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
