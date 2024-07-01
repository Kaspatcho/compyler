from lexer import lexer
from parse_symbols import parse_symbols
from sys import argv

_, test, *args = argv
symbols = lexer(test)
expression = parse_symbols(symbols)

if len(args) > 0 and '--tree' in args:
    if getattr(expression, 'print', False): expression.print()
    else: print(expression)
    print()

result = expression.execute()
if result: print('result:', result)
