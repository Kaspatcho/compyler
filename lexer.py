from symbols import Symbol, BuiltinFunction
from os.path import splitext

assert len(Symbol) == 25, 'lexer nao cobre todos os simbolos'


def match_keywords(word: str):
    match word:
        case 'if':
            return Symbol.If
        case 'else':
            return Symbol.Else
        case 'let':
            return Symbol.Let
        case 'while':
            return Symbol.While
        case _:
            builtin_functions = [x.name.lower() for x in BuiltinFunction]
            if word.lower() in builtin_functions: return BuiltinFunction[word.capitalize()]
            return word


def lexer(expression: str) -> list[Symbol]:
    symbols = []
    expr = list(expression.strip())

    while expr:
        c = expr.pop(0)
        match c:
            case ' ': continue
            case '+':
                symbols.append(Symbol.Plus)
            case '-':
                symbols.append(Symbol.Minus)
            case '%':
                symbols.append(Symbol.Percent)
            case '(':
                symbols.append(Symbol.OpenParen)
            case ')':
                symbols.append(Symbol.CloseParen)
            case '{':
                symbols.append(Symbol.OpenBracket)
            case '}':
                symbols.append(Symbol.CloseBracket)
            case ',':
                symbols.append(Symbol.Comma)
            case ';':
                symbols.append(Symbol.SemiColon)
            case '*':
                if len(expr) > 0 and expr[0] == '*':
                    symbols.append(Symbol.DoubleStar)
                    expr.pop(0)
                else: symbols.append(Symbol.Star)

            case '!':
                if len(expr) > 0 and expr[0] == '=':
                    symbols.append(Symbol.BangEqual)
                    expr.pop(0)
                else: symbols.append(Symbol.Bang)

            case '>':
                if len(expr) > 0 and expr[0] == '=':
                    symbols.append(Symbol.GreaterThanEqual)
                    expr.pop(0)
                else: symbols.append(Symbol.GreaterThan)

            case '<':
                if len(expr) > 0 and expr[0] == '=':
                    symbols.append(Symbol.LessThanEqual)
                    expr.pop(0)
                else: symbols.append(Symbol.LessThan)

            case '=':
                if len(expr) > 0 and expr[0] == '=':
                    symbols.append(Symbol.DoubleEqual)
                    expr.pop(0)
                else: symbols.append(Symbol.Equal)

            case '/':
                if len(expr) > 0 and expr[0] == '/':
                    symbols.append(Symbol.DoubleSlash)
                    expr.pop(0)
                else: symbols.append(Symbol.Slash)

            case c if c.isalpha():
                word = c
                while len(expr) > 0 and expr[0].isalnum(): word += expr.pop(0)
                symbols.append(match_keywords(word))

            case c if c.isdigit():
                while len(expr) > 0 and expr[0].isdigit(): c += expr.pop(0)
                symbols.append(int(c))

            case '"' | "'":
                s = ""
                while len(expr) > 0 and expr[0] != c: s += expr.pop(0)
                expr.pop(0)
                symbols.append(s)

            case _: raise Exception(f'nao sei oq é "{c}"')

    return symbols


def file_lexer(file: str):
    _, extension = splitext(file)
    if extension != '.wy':
        raise ImportError('file is not a .wy file')

    code = ''
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.endswith('}'): line += ';'
            code += line

    return lexer('{' + code + '}')
