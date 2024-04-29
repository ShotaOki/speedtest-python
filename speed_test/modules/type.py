from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ProcessType(str, Enum):
    threads = "threads"
    subprocess = "subprocess"
    subinterpreter = "subinterpreter"
    asyncprocess = "async"
    single = "single"
    subinterpreter_subproc = "subinterpreter_subproc"
    subinterpreter_threads = "subinterpreter_threads"


class ProcessTarget(str, Enum):
    s3 = "s3"
    bedrock = "bedrock"
    sts = "sts"
    curl_sts = "curl_sts"
    local = "local"
    curl = "curl"
    sleep = "sleep"


class InputType(BaseModel):
    type: ProcessType
    process_count: int
    target: ProcessTarget
    start_date: str = Field("")
    request_id: str = Field("")
    allow_to_await: int = Field(0)

    def setup(self):
        self.start_date = datetime.now().isoformat()

    @property
    def read_start_date(self):
        return datetime.fromisoformat(self.start_date)
