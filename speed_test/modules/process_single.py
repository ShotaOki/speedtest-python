from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType


class ProcessSingle(ProcessBase):

    def start(self, input: InputType, module: ModuleBase):
        for i in range(input.process_count):
            module.start(module.create_parameter(i, input))
