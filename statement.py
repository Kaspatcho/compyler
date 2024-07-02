from binary_expression import BinaryExpression
from typing import Optional
from block import Block


class IfStatement:
    def __init__(self, expression: BinaryExpression, block: Block, elseBlock: Optional[Block] = None) -> None:
        self.expression = expression
        self.block = block
        self.elseBlock = elseBlock

    def __repr__(self) -> str:
        return f'IfStatement(expr={self.expression}, block={self.block}, elseBlock={self.elseBlock})'

    def print(self, indentation=2):
        print((' ' * (indentation - 2)) + 'IfStatement')

        if isinstance(self.expression, BinaryExpression):
            self.expression.print(indentation + 2)
        else:
            print((' ' * indentation) + str(self.expression))

        print((' ' * indentation) + 'ThenStatement')
        if getattr(self.block, 'print', False):
            self.block.print(indentation + 2)
        else:
            print((' ' * indentation) + str(self.block))

        if self.elseBlock:
            print((' ' * indentation) + 'ElseStatement')
            if getattr(self.elseBlock, 'print', False):
                self.elseBlock.print(indentation + 2)
            else:
                print((' ' * indentation) + str(self.elseBlock))

        print((' ' * (indentation - 2)) + 'EndIf')

    def execute(self):
        result = self.expression.execute() if isinstance(self.expression, BinaryExpression) else self.expression

        if result == 1: return self.block.execute()
        elif self.elseBlock: return self.elseBlock.execute()


class WhileStatement:
    def __init__(self, condition: BinaryExpression, block: Block) -> None:
        self.condition = condition
        self.block = block

    def __repr__(self) -> str:
        return f'WhileStatement(condition={self.condition}, block={self.block})'

    def execute(self):
        condition = self.condition.execute() if hasattr(self.condition, 'execute') else self.condition
        while condition:
            self.block.execute()
            condition = self.condition.execute() if hasattr(self.condition, 'execute') else self.condition
