import threading
from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType
import _xxsubinterpreters as interpreters  # type: ignore


class ProcessThreadsSubinterpreter(ProcessBase):

    @staticmethod
    def _start_thread(processs_str: str, parameter):
        intp_id = interpreters.create()
        interpreters.run_string(intp_id, processs_str, shared=parameter)
        interpreters.destroy(intp_id)

    def start(self, input: InputType, module: ModuleBase):

        threads = []
        # サブインタープリターの実行
        for index in range(input.process_count):
            thread = threading.Thread(
                target=ProcessThreadsSubinterpreter._start_thread,
                args=(module.start_proc_str(), module.create_parameter(index, input)),
            )
            thread.start()
            threads.append(thread)

        # すべてのスレッドが完了するのを待つ
        for thread in threads:
            thread.join()

        pass
