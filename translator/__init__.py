from translator.lexical_analyzer import LexicalAnalyzer
from translator.syntax_analyzer import SyntaxAnalyzer
from translator.semantic_analyzer import SemanticAnalyzer
from translator.code_generator import CodeGenerator

from os.path import join as pj

class Translator:

    def __init__(self, code_folder, debug=False):
        self.code_folder = code_folder
        self.debug = debug

    def run(self, java_code):
        lexical_analyzer_instance = LexicalAnalyzer()
        syntax_analyzer_instance = SyntaxAnalyzer()
        semantic_analyzer_instance = SemanticAnalyzer()
        code_generator_instance = CodeGenerator()

        lexical_analyzer_output = lexical_analyzer_instance.run(java_code)
        if self.debug:
            with open(pj(self.code_folder, 'lexer.txt'), 'w') as debug_lexer:
                print('\n'.join(list(map(str, lexical_analyzer_output))), file=debug_lexer)
        syntax_analyzer_output = syntax_analyzer_instance.run(lexical_analyzer_output)
        # if self.debug:
        #     with open(pj(self.code_folder, 'rules.txt'), 'w') as debug_earley:
        #         print('\n'.join(reversed(list(map(str, syntax_analyzer_output)))), file=debug_earley)

        semantic_analyzer_output = semantic_analyzer_instance.run(syntax_analyzer_output)
        cpp_code = code_generator_instance.run(semantic_analyzer_output)

        return cpp_code
