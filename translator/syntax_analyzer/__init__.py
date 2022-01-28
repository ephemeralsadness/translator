from translator.syntax_analyzer.earley import make_right_parsing
from translator.syntax_analyzer.tree import build_tree


class SyntaxAnalyzer:

    def __init__(self):
        ...

    def run(self, token_list):
        rules = make_right_parsing(' '.join(token_list))
        root = build_tree(rules)
        return root


