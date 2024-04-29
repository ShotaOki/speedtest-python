import json
from time import perf_counter_ns
from modules.type import InputType, ProcessTarget, ProcessType
from modules.module_local import ModuleLocal
from modules.module_curl import ModuleCurl
from modules.module_sleep import ModuleSleep
from modules.module_sts import ModuleSts
from modules.module_curl_sts import ModuleCurlSts
from modules.module_curl_bedrock import ModuleCurlBedrock
from modules.process_subinterpret import ProcessSubinterpreter
from modules.process_threads import ProcessThreads
from modules.process_async import ProcessAsync
from modules.process_single import ProcessSingle
from modules.process_subprocess import ProcessSubprocess
from modules.process_subproc_subinterpret import ProcessSubprocessSubinterpreter
from modules.process_threads_subinterpret import ProcessThreadsSubinterpreter

# import requests


def lambda_handler(event, context):
    parameter = InputType.model_validate_json(event["body"])
    parameter.setup()
    start = perf_counter_ns()
    # =================================================================
    if parameter.target == ProcessTarget.local:
        module = ModuleLocal
    elif parameter.target == ProcessTarget.curl:
        module = ModuleCurl
        parameter.allow_to_await = 1
    elif parameter.target == ProcessTarget.sleep:
        module = ModuleSleep
        parameter.allow_to_await = 1
    elif parameter.target == ProcessTarget.sts:
        module = ModuleSts
    elif parameter.target == ProcessTarget.curl_sts:
        module = ModuleCurlSts
        parameter.allow_to_await = 1
    elif parameter.target == ProcessTarget.bedrock:
        module = ModuleCurlBedrock
        parameter.allow_to_await = 1
    # =================================================================
    if parameter.type in module.deny_list():
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "processing": parameter.type.value,
                    "module_name": parameter.target.value,
                    "result": "skip",
                }
            ),
        }
    # =================================================================
    if parameter.type == ProcessType.subinterpreter:
        ProcessSubinterpreter().start(parameter, module)
    elif parameter.type == ProcessType.threads:
        ProcessThreads().start(parameter, module)
    elif parameter.type == ProcessType.asyncprocess:
        ProcessAsync().start(parameter, module)
    elif parameter.type == ProcessType.single:
        ProcessSingle().start(parameter, module)
    elif parameter.type == ProcessType.subprocess:
        ProcessSubprocess().start(parameter, module)
    elif parameter.type == ProcessType.subinterpreter_subproc:
        ProcessSubprocessSubinterpreter().start(parameter, module)
    elif parameter.type == ProcessType.subinterpreter_threads:
        ProcessThreadsSubinterpreter().start(parameter, module)
    else:
        return
    response = json.dumps(
        {
            "processing": parameter.type.value,
            "module_name": parameter.target.value,
            "result": "done",
            "start": parameter.start_date,
            "duration": (perf_counter_ns() - start) / 10**9,
        }
    )
    print(response)
    return {"statusCode": 200, "body": response}
