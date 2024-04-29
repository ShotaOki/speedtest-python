from multiprocessing import Process
from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType
import _xxsubinterpreters as interpreters  # type: ignore


class ProcessSubprocessSubinterpreter(ProcessBase):

    @staticmethod
    def _start_thread(processs_str: str, parameter):
        intp_id = interpreters.create()
        interpreters.run_string(intp_id, processs_str, shared=parameter)
        interpreters.destroy(intp_id)

    def start(self, input: InputType, module: ModuleBase):
        proc_list = []
        for i in range(input.process_count):
            # サブインタープリターの実行
            proc = Process(
                target=ProcessSubprocessSubinterpreter._start_thread,
                args=(module.start_proc_str(), module.create_parameter(i, input)),
            )
            proc.start()
            proc_list.append(proc)
        for p in proc_list:
            p.join()
