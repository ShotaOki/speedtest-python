from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType
import _xxsubinterpreters as interpreters  # type: ignore


class ProcessSubinterpreter(ProcessBase):

    @staticmethod
    def _start_thread(processs_str: str, parameter):
        intp_id = interpreters.create()
        interpreters.run_string(intp_id, processs_str, shared=parameter)
        interpreters.destroy(intp_id)

    def start(self, input: InputType, module: ModuleBase):
        # サブインタープリターの実行
        for index in range(input.process_count):
            ProcessSubinterpreter._start_thread(
                module.start_proc_str(), module.create_parameter(index, input)
            )
