import json
from pathlib import Path
import sys
import gc
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "speed_test"))
from app import lambda_handler  # noqa

PROCESS_COUNT_REQUESTS = 1

PROCESSING = [
    # pytest.param("subinterpreter"),
    pytest.param("threads"),
    # pytest.param("async"),
    # pytest.param("single"),
    # pytest.param("subprocess"),
    # pytest.param("subinterpreter_subproc"),
    # pytest.param("subinterpreter_threads"),
]

TEST_PROCESS = [
    # "local",
    # "curl",
    # "sleep",
    # "curl_sts",
    # "bedrock",
    # "s3",
    "boto_s3"
]


@pytest.mark.parametrize("target", PROCESSING)
def test_local(target):
    for process in TEST_PROCESS:
        res = lambda_handler(
            {
                "body": json.dumps(
                    {
                        "request_id": "test",
                        "target": process,
                        "type": target,
                        "process_count": PROCESS_COUNT_REQUESTS,
                    }
                )
            },
            None,
        )
        print(res)
        gc.collect()
