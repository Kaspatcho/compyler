from symbols import Symbol, BuiltinFunction
from binary_expression import BinaryExpression
from statement import IfStatement
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

    if isinstance(symbols[0], BuiltinFunction):
        return parse_builtin(symbols)
    
    if isinstance(symbols[0], str):
        return symbols.pop(0)

    return parse_expression(symbols)


def parse_builtin(symbols):
    type = symbols.pop(0)
    assert len(symbols) > 0 and symbols[0] == Symbol.OpenParen, 'invalid syntax for function'
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
        assert len(symbols) > 0 and symbols[0] == Symbol.SemiColon, 'line without semicolon'
        symbols.pop(0)

    assert len(symbols) > 0 and symbols[0] == Symbol.CloseBracket, 'unclosed block'
    symbols.pop(0)

    return Block(lines)


def parse_statement(symbols: list):
    # get expression
    symbols.pop(0)
    assert len(symbols) > 0, 'invalid expression for statement'
    condition = symbols.pop(0)
    assert condition == Symbol.OpenParen, 'invalid expression for statement'
    condition = parse_expression(symbols)
    assert len(symbols) > 0 and symbols[0] == Symbol.CloseParen, 'invalid expression for statement'
    symbols.pop(0)

    # get blocks
    assert len(symbols) > 0, 'missing block for if statement'
    then_block = symbols.pop(0)
    else_block = None

    assert then_block == Symbol.OpenBracket, 'incorrect block for then statement'
    then_block = parse_block(symbols)

    if len(symbols) == 0: return IfStatement(condition, then_block, else_block)

    if symbols[0] == Symbol.Else:
        symbols.pop(0)
        a = symbols.pop(0)
        assert a == Symbol.OpenBracket, 'mission block for else statement'
        else_block = parse_block(symbols)

    if len(symbols) > 0 and symbols[0] == Symbol.CloseParen: symbols.pop(0)
    return IfStatement(condition, then_block, else_block)
