from modules.module_base import ModuleBase
from modules.type import InputType


class ModuleLocal(ModuleBase):

    @classmethod
    def create_parameter(cls, index: int, input: InputType):
        return {
            "process_count": 30,
            "start_date": ModuleBase.str_with_padding(input.start_date),
            "processing": ModuleBase.str_with_padding(input.type.value),
            "module_name": ModuleBase.str_with_padding(input.target.value),
            "request_id": ModuleBase.str_with_padding(input.request_id),
        }

    @classmethod
    def start(cls, parameter):
        process_count: int = parameter["process_count"]
        start_date: str = parameter["start_date"]
        processing: str = parameter["processing"]
        module_name: str = parameter["module_name"]
        request_id: str = parameter["request_id"]
        # END:PROC:HEADER
        from time import perf_counter_ns
        import datetime
        from decimal import Decimal
        import json

        start_date = start_date.strip()
        processing = processing.strip()
        module_name = module_name.strip()
        request_id = request_id.strip()

        start = perf_counter_ns()
        now = datetime.datetime.now()
        start_offset = datetime.datetime.fromisoformat(start_date)
        start_delta = now - start_offset

        # START PROCESS -----------------------

        def fib_r(seq):
            if seq <= 1:
                return seq
            return fib_r(seq - 1) + fib_r(seq - 2)

        res = fib_r(process_count)

        # END PROCESS -------------------------

        end_secs = Decimal(perf_counter_ns() - start) / Decimal(10**9)
        print(
            json.dumps(
                {
                    "result": res,
                    "elapsed_time": f"{end_secs}",
                    "start_delta": f"{start_delta.total_seconds()}",
                    "processing": processing,
                    "module_name": module_name,
                    "request_id": request_id,
                }
            )
        )
