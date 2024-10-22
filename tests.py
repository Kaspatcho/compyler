#!/bin/python3
from unittest import TestCase, main, mock
from lexer import lexer, file_lexer
import variable as var
from symbols import Symbol
from parse_symbols import parse_symbols
from contextlib import redirect_stdout
from io import StringIO


class TestLexer(TestCase):
    def test_add(self):
        symbols = lexer('1+1')
        self.assertEqual(symbols, [1, Symbol.Plus, 1])

    def test_sub(self):
        symbols = lexer('1-1')
        self.assertEqual(symbols, [1, Symbol.Minus, 1])

    def test_mult(self):
        symbols = lexer('2*2')
        self.assertEqual(symbols, [2, Symbol.Star, 2])

    def test_div(self):
        symbols = lexer('2/2')
        self.assertEqual(symbols, [2, Symbol.Slash, 2])

    def test_power(self):
        symbols = lexer('2**2')
        self.assertEqual(symbols, [2, Symbol.DoubleStar, 2])

    def test_intdiv(self):
        symbols = lexer('2//2')
        self.assertEqual(symbols, [2, Symbol.DoubleSlash, 2])

    def test_logical_op(self):
        symbols = lexer('== < > <= >= !=')
        expected = [
            Symbol.DoubleEqual, Symbol.LessThan, Symbol.GreaterThan,
            Symbol.LessThanEqual, Symbol.GreaterThanEqual, Symbol.BangEqual
        ]
        self.assertEqual(symbols, expected)

    def test_modulo(self):
        symbols = lexer('2%2')
        self.assertEqual(symbols, [2, Symbol.Percent, 2])

    def test_parens(self):
        symbols = lexer('(1+1)')
        self.assertEqual(symbols, [Symbol.OpenParen, 1, Symbol.Plus, 1, Symbol.CloseParen])

    def test_else(self):
        symbols = lexer('if else')
        self.assertEqual(symbols, [Symbol.If, Symbol.Else])

    def test_let(self):
        symbols = lexer('let a = 1')
        self.assertEqual(symbols, [Symbol.Let, 'a', Symbol.Equal, 1])


def expression(lexer_value: str = '', input_value: str = '', stdout: str = ''):
    def decorator(function: callable):
        def wrapper(self):
            io = StringIO()
            symbols = lexer(lexer_value)
            expression = parse_symbols(symbols)

            if input_value:
                original = mock.builtins.input
                mock.builtins.input = lambda _: input_value
            if stdout:
                with redirect_stdout(io): result = expression.execute()
                out = io.getvalue().strip()
                self.assertEqual(out, stdout)
            else: result = expression.execute()

            if input_value: mock.builtins.input = original

            function(self, result)
        return wrapper
    return decorator


class TestParser(TestCase):
    @expression(lexer_value='1+1')
    def test_add(self, result):
        self.assertEqual(result, 2)

    @expression(lexer_value='1-1')
    def test_sub(self, result):
        self.assertEqual(result, 0)

    @expression(lexer_value='2*2')
    def test_mult(self, result):
        self.assertEqual(result, 4)

    @expression(lexer_value='2/2')
    def test_div(self, result):
        self.assertEqual(result, 1)

    @expression(lexer_value='2%2')
    def test_modulo(self, result):
        self.assertEqual(result, 0)

    @expression(lexer_value='1+2*3')
    def test_op_order(self, result):
        self.assertEqual(result, 7)

    @expression(lexer_value='(1+2)')
    def test_parens(self, result):
        self.assertEqual(result, 3)

    @expression(lexer_value='(1+2)*3')
    def test_paren_order(self, result):
        self.assertEqual(result, 9)

    @expression(lexer_value='(2*(1+1))**2')
    def test_multiple_parens(self, result):
        self.assertEqual(result, 16)

    @expression(lexer_value='2 < 1')
    def test_false(self, result):
        self.assertEqual(result, 0)

    @expression(lexer_value='(2 > 1) * (1 < 2) * (3 != 1) * (2 >= 2) * (1 <= 2) * (2 == 2)')
    def test_operators(self, result):
        self.assertEqual(result, 1)


class TestStatement(TestCase):
    @expression(lexer_value='if (1+1 == 2) { 69; }')
    def test_if_true(self, result):
        self.assertEqual(result, 69)

    @expression(lexer_value='if (1 != 1) { 69; }')
    def test_if_false(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='if (1 == 1) { 69; } else { 420; }')
    def test_else_true(self, result):
        self.assertEqual(result, 69)

    @expression(lexer_value='if (1 != 1) { 69; } else { 420; }')
    def test_else_false(self, result):
        self.assertEqual(result, 420)

    @expression(lexer_value='(if (1 == 1) { 69 + 1; } else { 420; }) - 1')
    def test_expression_right(self, result):
        self.assertEqual(result, 69)

    @expression(lexer_value='1 + (if (1 != 1) { 69; } else { 420 - 1; })')
    def test_expression_left(self, result):
        self.assertEqual(result, 420)


class TestBuiltin(TestCase):
    @expression(lexer_value='read("")', input_value='bla')
    def test_input(self, result):
        self.assertEqual(result, 'bla')

    @expression(lexer_value='print(read(""))', input_value='blu', stdout='blu')
    def test_print_input(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='print(1)', stdout='1')
    def test_print(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='print(1, 2, 3)', stdout='1 2 3')
    def test_print_multiple(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='print("bla")', stdout='bla')
    def test_print_str(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='if (6%2 == 0) { print("even"); } else { print("odd"); }', stdout='even')
    def test_print_even(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='if (7%2 == 0) { print("even"); } else { print("odd"); }', stdout='odd')
    def test_print_odd(self, result):
        self.assertTrue(result is None)

    @expression(lexer_value='if (7%2 == 0) { print("even"); } else { print("odd"); 1; }', stdout='odd')
    def test_print_with_return(self, result):
        self.assertEqual(result, 1)

    def test_incorrect_read_type(self):
        with self.assertRaises(TypeError):
            symbols = lexer('read(1)')
            expression = parse_symbols(symbols)
            expression.execute()

    def test_read_with_no_argument(self):
        with self.assertRaises(TypeError):
            symbols = lexer('read()')
            expression = parse_symbols(symbols)
            expression.execute()


class TestVariable(TestCase):
    def tearDown(self) -> None:
        super().tearDown()
        var.VARIABLES.clear()

    @expression(lexer_value='let a=1')
    def test_assignment(self, result):
        self.assertEqual(result, 1)

    @expression(lexer_value='{let a=1; a=2;}')
    def test_setting_value(self, result):
        self.assertEqual(result, 2)

    def test_cannot_reset_variable(self):
        with self.assertRaises(TypeError):
            symbols = lexer('{let a=1; let a=2;}')
            parse_symbols(symbols)

    @expression(lexer_value='{let a=1+1;}')
    def test_variable_expression(self, result):
        self.assertEqual(result, 2)

    @expression(lexer_value='{let a = 2; a + 2; }')
    def test_expression_variable(self, result):
        self.assertEqual(result, 4)

    @expression(lexer_value='{let a = 19; if(a >= 18) { 1; } else {0; }; }')
    def test_conditions(self, result):
        self.assertEqual(result, 1)

    def test_incorrect_variable(self):
        with self.assertRaises(TypeError):
            symbols = lexer('let = 2')
            parse_symbols(symbols)

    def test_missing_equal(self):
        with self.assertRaises(SyntaxError):
            symbols = lexer('let a 2')
            parse_symbols(symbols)

    def test_missing_value(self):
        with self.assertRaises(SyntaxError):
            symbols = lexer('let a =')
            parse_symbols(symbols)


class TestWhile(TestCase):
    def tearDown(self) -> None:
        super().tearDown()
        var.VARIABLES.clear()

    @expression(lexer_value='{ let i=0; while(i < 10) { i = i+1; }; i; }')
    def test_loop(self, result):
        self.assertEqual(result, 10)

    @expression(lexer_value='{ let a=0; let b=1; let c=a; while (a<13) { c=a; a=b; b=c+b; }; a; }')
    def test_fibonacci(self, result):
        self.assertEqual(result, 13)


class TestFile(TestCase):
    def tearDown(self) -> None:
        super().tearDown()
        var.VARIABLES.clear()

    def test_fibonacci(self):
        io = StringIO()
        symbols = file_lexer('examples/fib.wy')
        expression = parse_symbols(symbols)

        with redirect_stdout(io): expression.execute()
        out = io.getvalue().strip()
        expected = '1\n1\n2\n3\n5\n8\n13'
        self.assertEqual(out, expected)

    def test_hello_world(self):
        io = StringIO()
        symbols = file_lexer('examples/hello-world.wy')
        expression = parse_symbols(symbols)

        with redirect_stdout(io): expression.execute()
        out = io.getvalue().strip()
        self.assertEqual(out, 'Hello, World!')

    def test_fizz_buzz(self):
        io = StringIO()
        symbols = file_lexer('examples/fizz-buzz.wy')
        expression = parse_symbols(symbols)

        with redirect_stdout(io): expression.execute()
        out = io.getvalue().strip()
        expected = '1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz'
        self.assertEqual(out, expected)


if __name__ == '__main__': main()
