# Compyler
simple code interpreter in python.

## Examples
```sh
$ python3 main.py '(2*(1+1))**2'
result: 16
```

```sh
$ python3 main.py '1+1' --tree
BinaryExpression
  1
  Symbol.Plus
  1

result: 2
```

```sh
$ python3 main.py 'if (1 == 1) { 69; } else { 420; }'
result: 69
```

```sh
$ python3 main.py '(if (1 != 1) { 69; } else { 420 + 1; }) - 1'
result: 420
```

```sh
$ python3 main.py 'print(1, 2, 3)'
1 2 3
```

```sh
$ python3 main.py 'print(read("what is your name: "))'
what is your name: percy jackson
percy jackson
```
