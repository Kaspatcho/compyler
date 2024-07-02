from lexer import lexer, file_lexer
from parse_symbols import parse_symbols
from sys import argv
from os.path import isfile

_, code, *args = argv
if isfile(code):
    symbols = file_lexer(code)
else:
    symbols = lexer(code)

expression = parse_symbols(symbols)

if len(args) > 0 and '--tree' in args:
    if getattr(expression, 'print', False): expression.print()
    else: print(expression)
    print()

result = expression.execute()
if result: print('result:', result)
