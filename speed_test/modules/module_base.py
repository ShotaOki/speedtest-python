from inspect import getsource
from textwrap import dedent
from modules.type import InputType, ProcessType
from typing import List


class ModuleBase:

    @staticmethod
    def deny_list() -> List[ProcessType]:
        return []

    @staticmethod
    def str_with_padding(value):
        return value + "     "

    @classmethod
    def create_parameter(cls, index: int, input: InputType):
        return {}

    @classmethod
    def start(cls, parameter):
        pass

    @classmethod
    async def start_async(cls, parameter):
        pass

    @classmethod
    def start_proc_str(cls):
        """
        関数を文字列に変換する
        """
        src = getsource(cls.start).split("# END:PROC:HEADER", maxsplit=1)[1]
        src = dedent(src)
        return src
