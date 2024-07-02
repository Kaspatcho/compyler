from typing import Dict
VARIABLES: Dict[str, 'Variable'] = dict()


class Variable:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
        if self.name in VARIABLES.keys():
            raise TypeError('already assigned this variable')
        VARIABLES[self.name] = self

    def __repr__(self) -> str:
        return f'Variable(name={self.name}, value={self.value})'

    def set(self, value):
        self.value = value
        return value

    def get(self):
        return self.value

    def execute(self):
        result = self.value.execute() if hasattr(self.value, 'execute') else self.value
        if result != self.value: self.value = result

        return result


class VariableAssignment:
    def __init__(self, reference: Variable, value) -> None:
        self.reference = reference
        self.value = value

    def __repr__(self) -> str:
        return f'VariableAssignment(reference={self.reference.name}, new_value={self.value})'

    def execute(self):
        result = self.value.execute() if hasattr(self.value, 'execute') else self.value
        return self.reference.set(result)
