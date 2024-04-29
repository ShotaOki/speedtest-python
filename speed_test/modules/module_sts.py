from typing import List
from modules.module_base import ModuleBase
from modules.type import InputType, ProcessType


class ModuleSts(ModuleBase):

    @staticmethod
    def deny_list() -> List[ProcessType]:
        return [
            ProcessType.subinterpreter,
            ProcessType.subinterpreter_threads,
            ProcessType.subinterpreter_subproc,
        ]

    @classmethod
    def create_parameter(cls, index: int, input: InputType):
        return {
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import json
        import boto3

        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        now = datetime.datetime.now()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = now - start_offset

        # START PROCESS -----------------------

        identity = boto3.client("sts").get_caller_identity()

        # END PROCESS -------------------------

        end_secs = Decimal(perf_counter_ns() - start) / Decimal(10**9)
        print(
            json.dumps(
                {
                    "result": len(identity["UserId"]),
                    "elapsed_time": f"{end_secs}",
                    "start_delta": f"{start_delta.total_seconds()}",
                    "processing": processing,
                    "module_name": module_name,
                    "request_id": request_id,
                }
            )
        )
