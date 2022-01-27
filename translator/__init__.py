from translator.lexical_analyzer import LexicalAnalyzer
from translator.syntax_analyzer import SyntaxAnalyzer
from translator.semantic_analyzer import SemanticAnalyzer
from translator.code_generator import CodeGenerator


class Translator:

    def __init__(self):
        ...

    def run(self, java_code):
        lexical_analyzer_instance = LexicalAnalyzer()
        syntax_analyzer_instance = SyntaxAnalyzer()
        semantic_analyzer_instance = SemanticAnalyzer()
        code_generator_instance = CodeGenerator()

        lexical_analyzer_output = lexical_analyzer_instance.run(java_code)
        syntax_analyzer_output = syntax_analyzer_instance.run(lexical_analyzer_output)
        semantic_analyzer_output = semantic_analyzer_instance.run(syntax_analyzer_output)
        cpp_code = code_generator_instance.run(semantic_analyzer_output)

        return cpp_code
