# Compyler
simple code interpreter in python.

## Examples
### Math expression
```sh
$ python3 main.py '(2*(1+1))**2'
result: 16
```

### With Syntax Tree
```sh
$ python3 main.py '1+1' --tree
BinaryExpression
  1
  Symbol.Plus
  1

result: 2
```

### if statement
```sh
$ python3 main.py 'if (1 == 1) { 69; } else { 420; }'
result: 69
```

### return of if block with math
```sh
$ python3 main.py '(if (1 != 1) { 69; } else { 420 + 1; }) - 1'
result: 420
```

### printing
```sh
$ python3 main.py 'print("hello, world!")'
hello, world!
```

### creating variables
```sh
$ python3 main.py '{ let a=1; print(a); }'
1
```

### reading input
```sh
$ python3 main.py '{ let name=read("what is your name? "); print(name); }'
what is your name? perry the platypus
perry the platypus
```
