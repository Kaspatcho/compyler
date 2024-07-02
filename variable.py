VARIABLES = dict()


class Variable:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
        if self.name in VARIABLES.keys():
            raise TypeError('already assigned this variable')
        VARIABLES[self.name] = self

    def set(self, value):
        self.value = value
        return value

    def execute(self):
        result = self.value.execute() if hasattr(self.value, 'execute') else self.value
        if result != self.value: self.value = result

        return result
