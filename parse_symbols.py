from symbols import Symbol, BuiltinFunction
from binary_expression import BinaryExpression
from statement import IfStatement
from variable import Variable, VARIABLES, VariableAssignment
from builtin import Builtin
from block import Block


def parse_expression(symbols: list):
    left = symbols.pop(0)
    if left == Symbol.OpenParen: left = parse_parens(symbols)
    if len(symbols) == 0: return left

    if symbols[0] == Symbol.CloseParen or symbols[0] == Symbol.SemiColon or symbols[0] == Symbol.Comma: return left
    op = symbols.pop(0)

    if symbols[0] == Symbol.SemiColon: return left

    right = symbols.pop(0)
    if right == Symbol.OpenParen: right = parse_parens(symbols)

    if len(symbols) == 0: return BinaryExpression(left, op, right)

    next_op = symbols[0]
    if next_op.value[1] > op.value[1]:
        symbols.insert(0, right)
        return BinaryExpression(left, op, parse_expression(symbols))
    else:
        expr = BinaryExpression(left, op, right)
        symbols.insert(0, expr)
        return parse_expression(symbols)


def parse_symbols(symbols: list):
    if symbols[0] == Symbol.OpenBracket:
        symbols.pop(0)
        return parse_block(symbols)

    if symbols[0] == Symbol.If:
        return parse_statement(symbols)

    if symbols[0] == Symbol.Let:
        return parse_let(symbols)

    if isinstance(symbols[0], BuiltinFunction):
        return parse_builtin(symbols)

    if isinstance(symbols[0], str) and symbols[0] in VARIABLES.keys():
        return parse_variable(symbols)

    if isinstance(symbols[0], str):
        return symbols.pop(0)

    return parse_expression(symbols)


def parse_builtin(symbols):
    type = symbols.pop(0)
    if len(symbols) < 0 or symbols[0] != Symbol.OpenParen:
        raise SyntaxError('invalid syntax for function')
    symbols.pop(0)
    args = parse_args(symbols)
    return Builtin(type, args)


def parse_args(symbols: list):
    a = []
    while len(symbols) > 0 and symbols[0] != Symbol.CloseParen:
        a.append(parse_symbols(symbols))
        if len(symbols) > 0 and symbols[0] == Symbol.Comma: symbols.pop(0)

    if len(symbols) > 0 and symbols[0] == Symbol.CloseParen: symbols.pop(0)

    return a


def parse_parens(symbols: list):
    expr = parse_symbols(symbols)
    if len(symbols) > 0 and symbols[0] == Symbol.CloseParen: symbols.pop(0)
    return expr


def parse_block(symbols: list):
    lines = []
    while len(symbols) > 0 and symbols[0] != Symbol.CloseBracket:
        lines.append(parse_symbols(symbols))
        if len(symbols) == 0 or symbols[0] != Symbol.SemiColon:
            raise SyntaxError('line without semicolon')
        symbols.pop(0)

    if len(symbols) == 0 or symbols[0] != Symbol.CloseBracket:
        raise SyntaxError('block without }')
    symbols.pop(0)

    return Block(lines)


def parse_let(symbols: list):
    symbols.pop(0)
    if len(symbols) == 0:
        raise SyntaxError('invalid let statement: missing variable name')

    name = symbols.pop(0)
    if not isinstance(name, str):
        raise TypeError('invalid variable name type')

    if len(symbols) == 0 or symbols[0] != Symbol.Equal:
        raise SyntaxError('invalid let statement: missing =')

    symbols.pop(0)

    if len(symbols) == 0:
        raise SyntaxError('invalid let statement: missing value')

    value = parse_symbols(symbols)

    return Variable(name, value)


def parse_variable(symbols: list):
    name = symbols.pop(0)
    if name not in VARIABLES.keys():
        raise NameError(f'unknown variable "{name}"')

    variable = VARIABLES[name]

    if len(symbols) > 0 and symbols[0] == Symbol.Equal:
        symbols.pop(0)
        if len(symbols) == 0:
            raise SyntaxError('invalid variable assignment: missing value')

        value = parse_symbols(symbols)
        return VariableAssignment(variable, value)

    symbols.insert(0, variable)
    return parse_symbols(symbols)


def parse_statement(symbols: list):
    # get expression
    symbols.pop(0)
    if len(symbols) == 0:
        raise SyntaxError('invalid expression for statement')

    condition = symbols.pop(0)
    if condition != Symbol.OpenParen:
        raise SyntaxError('invalid statement: missing (')

    condition = parse_expression(symbols)
    if len(symbols) == 0 or symbols[0] != Symbol.CloseParen:
        raise SyntaxError('invalid expression for statement')

    symbols.pop(0)

    # get blocks
    if len(symbols) == 0:
        raise SyntaxError('missing block for if statement')
    then_block = symbols.pop(0)
    else_block = None

    if then_block != Symbol.OpenBracket:
        raise SyntaxError('incorrect block for then statement')

    then_block = parse_block(symbols)

    if len(symbols) == 0: return IfStatement(condition, then_block, else_block)

    if symbols[0] == Symbol.Else:
        symbols.pop(0)
        a = symbols.pop(0)
        if a != Symbol.OpenBracket:
            raise SyntaxError('mission block for else statement')

        else_block = parse_block(symbols)

    if len(symbols) > 0 and symbols[0] == Symbol.CloseParen: symbols.pop(0)
    return IfStatement(condition, then_block, else_block)
