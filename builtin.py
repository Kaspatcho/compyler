from binary_expression import BinaryExpression
from symbols import BuiltinFunction
from typing import List

assert len(BuiltinFunction) == 2, 'Builtin nao cobre todas as funcoes'


class Builtin:
    def __init__(self, type: BuiltinFunction, args: List[BinaryExpression]) -> None:
        self.type = type
        self.args = args

    def __repr__(self) -> str:
        return f'Buitin(type={self.type}, args={self.args})'

    def execute(self):
        match self.type:
            case BuiltinFunction.Print:
                args = [arg if not getattr(arg, 'execute', False) else arg.execute() for arg in self.args]
                print(*args)
                return

            case BuiltinFunction.Read:
                if len(self.args) != 1:
                    raise TypeError('input should have one argument')

                if not isinstance(self.args[0], str):
                    raise TypeError('read argument must be a string')

                return input(self.args[0])
            case _:
                raise NameError(f'unknown function "{self.type}"')
