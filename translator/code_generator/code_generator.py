
class GeneratorManager:
    def __init__(self):
        self.buffer_lines = []
        self.line = ''
        self.tabs = 0

    def print(self, s):
        self.line += s

    def println(self, s=''):
        self.line += s
        self.buffer_lines.append('\t' * self.tabs + self.line)
        self.line = ''

    def increase_tabs(self):
        self.tabs += 1

    def decrease_tabs(self):
        if self.tabs == 0:
            raise Exception('Compiler error: bad decreasing tabs')
        self.tabs -= 1

    def get_code(self):
        self.buffer_lines.append('\t' * self.tabs + self.line)
        return '\n'.join(self.buffer_lines)


generator_manager = GeneratorManager()
