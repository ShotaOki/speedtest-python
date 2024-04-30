import threading
from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType


class ProcessThreads(ProcessBase):

    def start(self, input: InputType, module: ModuleBase):

        threads = []
        # スレッドの実行
        for index in range(input.process_count):
            thread = threading.Thread(
                target=module.start,
                args=(module.create_parameter(index, input),),
            )
            thread.start()
            threads.append(thread)

        # すべてのスレッドが完了するのを待つ
        for thread in threads:
            thread.join()
