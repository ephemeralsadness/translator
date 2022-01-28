from translator.code_generator.code_generator import generator_manager

class CodeGenerator:

    def __init__(self):
        ...

    def run(self, root):
        root.generate()
        return generator_manager.get_code()
