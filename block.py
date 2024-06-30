class Block:
    def __init__(self, lines: list) -> None:
        self.lines = lines

    def __repr__(self) -> str:
        return f'Block({self.lines})'

    def __str__(self) -> str:
        return f'Block({self.lines})'

    def execute(self):
        res = None
        for line in self.lines:
            res = line.execute() if getattr(line, 'execute', False) else line
        else:
            return res
