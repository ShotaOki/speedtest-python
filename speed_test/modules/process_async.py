import asyncio
from modules.process_base import ProcessBase
from modules.module_base import ModuleBase
from modules.type import InputType


class ProcessAsync(ProcessBase):

    @staticmethod
    async def async_process(module: ModuleBase, index: int, input: InputType):
        if input.allow_to_await == 0:
            module.start(module.create_parameter(index, input))
        else:
            await module.start_async(module.create_parameter(index, input))

    @staticmethod
    async def execute(input: InputType, module: ModuleBase):
        task_list = [
            asyncio.create_task(ProcessAsync.async_process(module, i, input))
            for i in range(input.process_count)
        ]
        for task in task_list:
            await task

    def start(self, input: InputType, module: ModuleBase):
        # スレッドの実行
        asyncio.run(ProcessAsync.execute(input, module))
