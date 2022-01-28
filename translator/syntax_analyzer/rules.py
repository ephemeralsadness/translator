import string
from translator.classes import *
from translator.constants import *


class Rule(object):
    def __init__(self, lhs, rhs, cls=None, **kwargs):
        self.lhs = lhs
        self.rhs = rhs
        self.cls = cls
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.lhs} -> {" ".join(self.rhs)}'


def ct(a):
    b = []
    for x in a:
        b.append(x)
        b.append(' ')
    b.pop(len(b) - 1)
    c = []
    for x in b:
        if x == '`':
            c.append(x)
        elif '~' in x:
            c.append(x)
        else:
            c += list(x)
    return c


java_rules = [
    Rule('~program~',
         ct(['class', '~identifier~', '{', '~main_function~', '}']),
         ),
    Rule('~program~',
         ct(['class', '~identifier~', '{', '~functions_declaration~', '~main_function~', '}']),
         ),

    Rule('~identifier~',
         ['~identifier_start~'],
         ),
    Rule('~identifier~',
         ['~identifier_start~', '~identifier_next~'],
         ),

    Rule('~identifier_start~',
         ['~letter~'],
         ),
    Rule('~identifier_start~',
         ['_'],
         ),

    *[
        Rule('~letter~',
             [i],
             )
        for i in LETTERS
    ],

    Rule('~identifier_next~',
         ['~identifier_start~', '~identifier_next~'],
         ),
    Rule('~identifier_next~',
         ['~digit~', '~identifier_next~'],
         ),
    Rule('~identifier_next~',
         ['~identifier_start~'],
         ),
    Rule('~identifier_next~',
         ['~digit~'],
         ),

    *[
        Rule('~digit~',
             [str(i)],
             )
        for i in range(0, 10)
    ],

    Rule('~main_function~',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '~function_body~', '}']),
         ),
    Rule('~main_function~',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '}']),
         ),

    Rule('~code_field~',
         ct(['~instruction~', '~code_field~']),
         ),
    Rule('~code_field~',
         ct(['~instruction~']),
         ),

    Rule('~instruction~',
         ct(['~assignment~', ';']),
         ),
    Rule('~instruction~',
         ct(['~var_declaration~', ';']),
         ),
    Rule('~instruction~',
         ct(['~function_call~', ';']),
         ),
    Rule('~instruction~',
         ct(['~expression~', ';']),
         ),
    Rule('~instruction~',
         ['~cycle~'],
         ),
    Rule('~instruction~',
         ['~if_operator~'],
         ),
    Rule('~instruction~',
         ct(['~function_return~', ';']),
         ),

    Rule('~assignment~',
         ct(['~identifier~', '~operator_assignment~', '~expression~']),
         ),

    *[
        Rule('~operator_assignment~',
             ct([i]),
             )
        for i in ASSIGNMENT_OPERATORS
    ],

    Rule('~expression~',
         ['~logical_expression~'],
         ),
    Rule('~expression~',
         ['~math_expression~'],
         ),
    Rule('~expression~',
         ['~symb_value~'],
         ),
    Rule('~expression~',
         ['~identifier~'],
         ),
    Rule('~expression~',
         ['~function_call~'],
         ),
    Rule('~expression~',
         ['~string_literal~'],
         ),

    Rule('~logical_expression~',
         ['~boolean_value~'],
         ),
    Rule('~logical_expression~',
         ct(['~math_expression~', '~compare_operator~', '~math_expression~']),
         ),
    Rule('~logical_expression~',
         ct(['~symb_value~', '~compare_operator~', '~symb_value~']),
         ),
    Rule('~logical_expression~',
         ct(['~logical_expression~', '&&', '~logical_expression~']),
         ),
    Rule('~logical_expression~',
         ct(['~logical_expression~', '||', '~logical_expression~']),
         ),
    Rule('~logical_expression~',
         ct(['(', '~logical_expression~', ')']),
         ),

    Rule('~math_expression~',
         ['~number~'],
         ),
    Rule('~math_expression~',
         ['~identifier~'],
         ),
    Rule('~math_expression~',
         ['~function_call~'],
         ),
    Rule('~math_expression~',
         ct(['~math_expression~', '~addition_sign~', '~math_expression~']),
         ),
    Rule('~math_expression~',
         ct(['~math_expression~', '~multiplication_sign~', '~math_expression~']),
         ),
    Rule('~math_expression~',
         ct(['(', '~math_expression~', ')']),
         ),
    Rule('~math_expression~',
         ['-', '~math_expression~'],
         ),

    *[
        Rule('~addition_sign~',
             [i],
             )
        for i in ['-', '+']
    ],

    *[
        Rule('~multiplication_sign~',
             [i],
             )
        for i in ['*', '/', '%']
    ],

    Rule('~number~',
         ['~integer~'],
         ),
    Rule('~number~',
         ['~real_number~'],
         ),

    Rule('~integer~',
         ['~digit~', '~integer~'],
         ),
    Rule('~integer~',
         ['~digit~'],
         ),

    Rule('~real_number~',
         ['~integer~', '.', '~integer~'],
         ),

    *[
        Rule('~compare_operator~',
             ct([i]),
             )
        for i in COMPARISON_OPERATORS
    ],

    Rule('~symb_value~',
         ["'", '~letter~', "'"],
         ),
    Rule('~symb_value~',
         ["'", '~digit~', "'"],
         ),
    Rule('~symb_value~',
         ["'", '~other_symb~', "'"],
         ),

    *[
        Rule('~other_symb~',
             [i],
             )
        for i in OTHER_SYMBOLS
    ],

    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '~code_field~', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '~code_field~', '}', 'else', '{', '~code_field~', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '~code_field~', '}', 'else', '{', '~if_operator~', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '}', 'else', '{', '~code_field~', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '~code_field~', '}', 'else', '{', '}']),
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~expression~', ')' '{', '}', 'else', '{', '~if_operator~', '}']),
         ),

    *[
        Rule('~boolean_value~',
             ct([i]),
             )
        for i in ['true', 'false']
    ],

    Rule('~functions_declaration~',
         ct(['static', '~function_type~', '~identifier~',
             '(', '~function_params~', ')', '(', '~function_body~', ')', '~functions_declaration~']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '(', '~function_body~', ')']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_type~', '~identifier~',
             '(', ')', '(', '~function_body~', ')', '~functions_declaration~']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '(', '~function_body~', ')']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_type~', '~identifier~',
             '(', '~function_params~', ')', '(', ')', '~functions_declaration~']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '(', ')']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_type~', '~identifier~',
             '(', ')', '(', ')', '~functions_declaration~']),
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '(', ')']),
         ),

    Rule('~function_return_type~',
         ['~type~'],
         ),
    Rule('~function_return_type~',
         ct(['void']),
         ),

    Rule('~type~',
         ['~valuable_type~'],
         ),

    *[
        Rule('~valuable_type~',
             ct([i]),
             )
        for i in VARIABLE_TYPES
    ],

    Rule('~function_params~',
         ct(['~valuable_type~', '~identifier~']),
         ),
    Rule('~function_params~',
         ct(['~valuable_type~', '~identifier~', ',', '~function_params~']),
         ),

    Rule('~function_body~',
         ['~code_field~'],
         ),

    Rule('~function_return~',
         ct(['return ', '~expression~']),
         ),

    Rule('~var_declaration~',
         ct(['~valuable_type~', '~identifier~'])
         ),
    Rule('~var_declaration~',
         ct(['~valuable_type~', '~identifier~', '=', '~expression~'])
         ),

    Rule('~function_call~',
         ct(['~identifier~', '(', '~function_call_params~', ')'])
         ),
    Rule('~function_call~',
         ct(['~identifier~', '(', ')'])
         ),
    Rule('~function_call~',
         ct(['System.out.println', '(', '~function_call_params~', ')'])
         ),
    Rule('~function_call~',
         ct(['System.out.print', '(', '~function_call_params~', ')'])
         ),
    Rule('~function_call~',
         ct(['Math.max', '(', '~function_call_params~', ')'])
         ),
    Rule('~function_call~',
         ct(['Math.min', '(', '~function_call_params~', ')'])
         ),

    Rule('~function_call_params~',
         ['~expression~'],
         ),
    Rule('~function_call_params~',
         ct(['~expression~', ',', '~function_call_params~'])
         ),

    Rule('~cycle~',
         ct(['while', '(', '~logical_expression~', ')', '{', '~code_field~', '}']),
         ),
    Rule('~cycle~',
         ct(['do', '{', '~code_field~', '}', 'while', '(', '~logical_expression~', ')', ';']),
         ),
    Rule('~cycle~',
         ct(['for', '(', '~var_declaration~', ';', '~logical_expression~', ';', '~assignment~', ')' '{', '~code_field~',
             '}']),
         ),
    Rule('~cycle~',
         ct(['for', '(', '~assignment~', ';', '~logical_expression~', ';', '~assignment~', ')' '{', '~code_field~',
             '}']),
         ),
    Rule('~cycle~',
         ct(['while', '(', '~logical_expression~', ')', '{', '}']),
         ),
    Rule('~cycle~',
         ct(['do', '{', '}', 'while', '(', '~logical_expression~', ')', ';']),
         ),
    Rule('~cycle~',
         ct(['for', '(', '~var_declaration~', ';', '~logical_expression~', ';', '~assignment~', ')' '{',
             '}']),
         ),
    Rule('~cycle~',
         ct(['for', '(', '~assignment~', ';', '~logical_expression~', ';', '~assignment~', ')' '{',
             '}']),
         ),

    Rule('~string_literal~',
         ['"', '~string_letters~', '"'],
         ),
    Rule('~string_literal~',
         ['"', '"'],
         ),

    Rule('~string_letters~',
         ['~letter~', '~string_letters~'],
         ),
    Rule('~string_letters~',
         ['~digit~', '~string_letters~'],
         ),
    Rule('~string_letters~',
         ['~other_symb~', '~string_letters~'],
         ),
    Rule('~string_letters~',
         ['~letter~'],
         ),
    Rule('~string_letters~',
         ['~digit~'],
         ),
    Rule('~string_letters~',
         ['~other_symb~'],
         ),
]
