from multiprocessing import Process
from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType


class ProcessSubprocess(ProcessBase):

    def start(self, input: InputType, module: ModuleBase):
        proc_list = []
        for i in range(input.process_count):
            proc = Process(
                target=module.start, args=(module.create_parameter(i, input),)
            )
            proc.start()
            proc_list.append(proc)
        for p in proc_list:
            p.join()
