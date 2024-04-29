import json
from modules.module_base import ModuleBase
from modules.type import InputType
import boto3
from botocore.config import Config

BUCKET_NAME = "datastore-20240429-speedtest"
FILES = [
    "2e029d6a423a20332bec0a759a916c72.png",
    "7fb3cf241f747ab52c3e6037e6129bff.png",
    "33c57611cb27e20d17366152507d2ec7.png",
    "92fe50623233958604c903cd7df1feab.png",
    "ae9031329652b55a3cf8cad4516477f3.png",
    "ca11af11062a02a1e41e126a47790d4e.png",
    "0c1f76d7156e51a67936cab060ba0780.png",
    "4cc6ea269141283bcf3a22669cef9ec4.png",
    "9d9361c013f2d41d19189edbcee0ea1a.png",
    "dbaffffcdacce7ef3b677d6d0ab01a2e.png",
]


class ModuleCurlS3(ModuleBase):
    @classmethod
    def create_parameter(cls, index: int, input: InputType):

        s3 = boto3.client("s3")
        my_config = Config(region_name="ap-northeast-1", signature_version="s3v4")
        s3 = boto3.client("s3", config=my_config)
        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": FILES[index],
            },
            ExpiresIn=3600,
        )

        return {
            "presigned_url": ModuleBase.str_with_padding(presigned_url),
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        presigned_url: str = parameter["presigned_url"]
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import urllib3
        import json

        presigned_url = presigned_url.strip()
        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = datetime.datetime.now() - start_offset

        # START PROCESS -----------------------

        response = urllib3.PoolManager().request(method="get", url=presigned_url)
        res = response.data

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
        presigned_url: str = parameter["presigned_url"]
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import aiohttp
        from aiohttp.client import URL

        presigned_url = presigned_url.strip()
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
                method="get",
                url=URL(presigned_url, encoded=True),
            ) as response:
                res = await response.read()

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
