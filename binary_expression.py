from symbols import Symbol

assert len(Symbol) == 23, 'BinaryExpression nao cobre todos os simbolos'

class BinaryExpression:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self) -> str:
        return f'BinaryExpression({self.left}, {self.op}, {self.right})'
    
    def print(self, indentation=2):
        print((' ' * (indentation - 2)) + 'BinaryExpression')

        if getattr(self.left, 'print', False):
            self.left.print(indentation + 2)
        else:
            print((' ' * indentation) + str(self.left))
        
        print((' ' * indentation) + str(self.op))

        if getattr(self.right, 'print', False):
            self.right.print(indentation + 2)
        else:
            print((' ' * indentation) + str(self.right))

    
    def execute(self):
        a = getattr(self.left, 'execute', None)
        b = getattr(self.right, 'execute', None)
        a = a() if a else self.left
        b = b() if b else self.right

        match self.op:
            case Symbol.Plus:
                return a + b
            case Symbol.Minus:
                return a - b
            case Symbol.Star:
                return a * b
            case Symbol.Slash:
                return a / b
            case Symbol.BangEqual:
                return int(a != b)
            case Symbol.DoubleEqual:
                return int(a == b)
            case Symbol.DoubleStar:
                return a ** b
            case Symbol.DoubleSlash:
                return a // b
            case Symbol.GreaterThan:
                return int(a > b)
            case Symbol.GreaterThanEqual:
                return int(a >= b)
            case Symbol.LessThan:
                return int(a < b)
            case Symbol.LessThanEqual:
                return int(a <= b)
            case Symbol.Percent:
                return a % b
            case Symbol.OpenBracket, Symbol.CloseParen, Symbol.SemiColon: pass
            case _:
                raise Exception(f'nao conheco o simbolo "{self.op}"')