VARIABLES = dict()


class Variable:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
        assert self.name not in VARIABLES.keys(), 'already assigned this variable'
        VARIABLES[self.name] = self

    def set(self, value):
        self.value = value
        return value

    def execute(self):
        result = self.value.execute() if hasattr(self.value, 'execute') else self.value
        if result != self.value: self.value = result

        return result


def assign_variable(name, value):
    assert name not in VARIABLES.keys(), 'already assigned this variable'
    VARIABLES[name] = value
    return value


def set_variable(name, value):
    VARIABLES[name] = value
    return value
