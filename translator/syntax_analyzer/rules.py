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
         ProgramDGN,
         functions=False),
    Rule('~program~',
         ct(['class', '~identifier~', '{', '~functions_declaration~', '~main_function~', '}']),
         ProgramDGN,
         functions=True),

    Rule('~identifier~',
         ['~identifier_start~'],
         IdentifierDGN,
         is_one_letter=True),
    Rule('~identifier~',
         ['~identifier_start~', '~identifier_next~'],
         IdentifierDGN,
         is_one_letter=False),

    Rule('~identifier_start~',
         ['~letter~'],
         IdentifierStartDGN,
         ),

    *[
        Rule('~letter~',
             [i],
             LetterDGN,
             )
        for i in LETTERS
    ],

    Rule('~identifier_next~',
         ['~identifier_start~', '~identifier_next~'],
         IdentifierNextDGN,
         is_digit=False,
         is_one_letter=False),
    Rule('~identifier_next~',
         ['~digit~', '~identifier_next~'],
         IdentifierNextDGN,
         is_digit=False,
         is_one_letter=False
         ),
    Rule('~identifier_next~',
         ['~identifier_start~'],
         IdentifierNextDGN,
         is_digit=False,
         is_one_letter=True
         ),
    Rule('~identifier_next~',
         ['~digit~'],
         IdentifierNextDGN,
         is_digit=True,
         is_one_letter=False
         ),

    *[
        Rule('~digit~',
             [str(i)],
             DigitDGN)
        for i in range(0, 10)
    ],

    Rule('~main_function~',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '~function_body~', '}']),
         MainFunctionDGN,
         has_body=True),
    Rule('~main_function~',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '}']),
         MainFunctionDGN,
         has_body=False
         ),

    Rule('~code_field~',
         ct(['~instruction~', '~code_field~']),
         CodeFieldDGN,
         has_code_field=True),
    Rule('~code_field~',
         ct(['~instruction~']),
         CodeFieldDGN,
         has_code_field=False
         ),

    Rule('~instruction~',
         ct(['~assignment~', ';']),
         InstructionDGN,
         what='assignment'),
    Rule('~instruction~',
         ct(['~var_declaration~', ';']),
         InstructionDGN,
         what='var_declaration'
         ),
    Rule('~instruction~',
         ct(['~function_call~', ';']),
         InstructionDGN,
         what='function_call'
         ),
    Rule('~instruction~',
         ct(['~expression~', ';']),
         InstructionDGN,
         what='expression'
         ),
    Rule('~instruction~',
         ['~cycle~'],
         InstructionDGN,
         what='cycle'
         ),
    Rule('~instruction~',
         ['~if_operator~'],
         InstructionDGN,
         what='if_operator'
         ),
    Rule('~instruction~',
         ct(['~function_return~', ';']),
         InstructionDGN,
         what='function_return'
         ),

    Rule('~assignment~',
         ct(['~identifier~', '~operator_assignment~', '~expression~']),
         AssignmentDGN),

    *[
        Rule('~operator_assignment~',
             ct([i]),
             OperatorAssignmentDGN)
        for i in ASSIGNMENT_OPERATORS
    ],

    Rule('~expression~',
         ['~logical_expression~'],
         ExpressionDGN,
         what='logical_expression'),
    Rule('~expression~',
         ['~math_expression~'],
         ExpressionDGN,
         what='math_expression'
         ),
    Rule('~expression~',
         ['~symb_value~'],
         ExpressionDGN,
         what='symb_value'
         ),
    Rule('~expression~',
         ['~identifier~'],
         ExpressionDGN,
         what='identifier'
         ),
    Rule('~expression~',
         ['~function_call~'],
         ExpressionDGN,
         what='function_call'
         ),
    Rule('~expression~',
         ['~string_literal~'],
         ExpressionDGN,
         what='string_literal'
         ),

    Rule('~logical_expression~',
         ['~boolean_value~'],
         LogicalExpressionDGN,
         what='boolean_value'),
    Rule('~logical_expression~',
         ct(['~math_expression~', '~compare_operator~', '~math_expression~']),
         LogicalExpressionDGN,
         what='math_comparison'
         ),
    Rule('~logical_expression~',
         ct(['~symb_value~', '~compare_operator~', '~symb_value~']),
         LogicalExpressionDGN,
         what='symb_comparison'
         ),
    Rule('~logical_expression~',
         ct(['~logical_expression~', '&&', '~logical_expression~']),
         LogicalExpressionDGN,
         what='&&'
         ),
    Rule('~logical_expression~',
         ct(['~logical_expression~', '||', '~logical_expression~']),
         LogicalExpressionDGN,
         what='||'
         ),
    Rule('~logical_expression~',
         ct(['(', '~logical_expression~', ')']),
         LogicalExpressionDGN,
         what='braced'
         ),

    Rule('~math_expression~',
         ['~number~'],
         MathExpressionDGN,
         what='number'),
    Rule('~math_expression~',
         ['~identifier~'],
         MathExpressionDGN,
         what='identifier'
         ),
    Rule('~math_expression~',
         ['~function_call~'],
         MathExpressionDGN,
         what='function_call'
         ),
    Rule('~math_expression~',
         ct(['~math_expression~', '~addition_sign~', '~math_expression~']),
         MathExpressionDGN,
         what='+'
         ),
    Rule('~math_expression~',
         ct(['~math_expression~', '~multiplication_sign~', '~math_expression~']),
         MathExpressionDGN,
         what='*'
         ),
    Rule('~math_expression~',
         ct(['(', '~math_expression~', ')']),
         MathExpressionDGN,
         what='braced'
         ),
    Rule('~math_expression~',
         ['-', '~math_expression~'],
         MathExpressionDGN,
         what='unary_minus'
         ),

    *[
        Rule('~addition_sign~',
             [i],
             AdditionSignDGN)
        for i in ['-', '+']
    ],

    *[
        Rule('~multiplication_sign~',
             [i],
             MultiplicationSignDGN)
        for i in ['*', '/', '%']
    ],

    Rule('~number~',
         ['~integer~'],
         NumberDGN,
         what='integer'),
    Rule('~number~',
         ['~real_number~'],
         NumberDGN,
         what='real_number'
         ),

    Rule('~integer~',
         ['~digit~', '~integer~'],
         IntegerDGN,
         is_one_digit=False),
    Rule('~integer~',
         ['~digit~'],
         IntegerDGN,
         is_one_digit=True
         ),

    Rule('~real_number~',
         ['~integer~', '.', '~integer~'],
         RealNumberDGN),

    *[
        Rule('~compare_operator~',
             ct([i]),
             CompareOperatorDGN)
        for i in COMPARISON_OPERATORS
    ],

    Rule('~symb_value~',
         ["'", '~letter~', "'"],
         SymbValueDGN),
    Rule('~symb_value~',
         ["'", '~digit~', "'"],
         SymbValueDGN),
    Rule('~symb_value~',
         ["'", '~other_symb~', "'"],
         SymbValueDGN),

    *[
        Rule('~other_symb~',
             [i],
             OtherSymbDGN)
        for i in OTHER_SYMBOLS
    ],

    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '~code_field~', '}']),
         IfOperatorDGN,
         what='if',
         has_empty_if_body=False,
         has_empty_else_body=False),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '~code_field~', '}', 'else', '{', '~code_field~', '}']),
         IfOperatorDGN,
         what='if-else',
         has_empty_if_body=False,
         has_empty_else_body=False
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '~code_field~', '}', 'else', '~if_operator~']),
         IfOperatorDGN,
         what='if-else-if',
         has_empty_if_body=False,
         has_empty_else_body=False
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '}']),
         IfOperatorDGN,
         what='if',
         has_empty_if_body=True,
         has_empty_else_body=False
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '}', 'else', '{', '~code_field~', '}']),
         IfOperatorDGN,
         what='if-else',
         has_empty_if_body=True,
         has_empty_else_body=False
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '~code_field~', '}', 'else', '{', '}']),
         IfOperatorDGN,
         what='if-else',
         has_empty_if_body=False,
         has_empty_else_body=True
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '}', 'else', '~if_operator~']),
         IfOperatorDGN,
         what='if-else-if',
         has_empty_if_body=True,
         has_empty_else_body=False
         ),
    Rule('~if_operator~',
         ct(['if', '(', '~logical_expression~', ')', '{', '}', 'else', '{', '}']),
         IfOperatorDGN,
         what='if-else',
         has_empty_if_body=True,
         has_empty_else_body=True
         ),

    *[
        Rule('~boolean_value~',
             ct([i]),
             BooleanValueDGN)
        for i in ['true', 'false']
    ],

    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '{', '~function_body~', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=True,
         has_body=True),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '{', '~function_body~', '}']),
         FunctionsDeclarationDGN,
         multiple_declarations=False,
         has_params=True,
         has_body=True
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '~function_body~', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=False,
         has_body=True
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '~function_body~', '}']),
         FunctionsDeclarationDGN,
         multiple_declarations=False,
         has_params=False,
         has_body=True
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '{', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=True,
         has_body=False
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '{', '}']),
         FunctionsDeclarationDGN,
         multiple_declarations=False,
         has_params=True,
         has_body=False
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=False,
         has_body=False
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '}']),
         FunctionsDeclarationDGN,
         multiple_declarations=False,
         has_params=False,
         has_body=False
         ),

    Rule('~function_return_type~',
         ['~type~'],
         FunctionReturnTypeDGN,
         is_void=False),
    Rule('~function_return_type~',
         ct(['void']),
         FunctionReturnTypeDGN,
         is_void=True
         ),

    Rule('~type~',
         ['~valuable_type~'],
         TypeDGN),

    *[
        Rule('~valuable_type~',
             ct([i]),
             ValuableTypeDGN)
        for i in VARIABLE_TYPES
    ],

    Rule('~function_params~',
         ct(['~valuable_type~', '~identifier~']),
         FunctionParamsDGN,
         is_multiple=False),
    Rule('~function_params~',
         ct(['~valuable_type~', '~identifier~', ',', '~function_params~']),
         FunctionParamsDGN,
         is_multiple=True
         ),

    Rule('~function_body~',
         ['~code_field~'],
         FunctionBodyDGN),

    Rule('~function_return~',
         ct(['return', '~expression~']),
         FunctionReturnDGN),

    Rule('~var_declaration~',
         ct(['~valuable_type~', '~identifier~']),
         VarDeclarationDGN,
         is_initialized=False),
    Rule('~var_declaration~',
         ct(['~valuable_type~', '~identifier~', '=', '~expression~']),
         VarDeclarationDGN,
         is_initialized=True
            ),

    Rule('~function_call~',
         ct(['~identifier~', '(', '~function_call_params~', ')']),
         FunctionCallDGN,
         has_params=True,
         name=None),
    Rule('~function_call~',
         ct(['~identifier~', '(', ')']),
         FunctionCallDGN,
         has_params=False,
         name=None
         ),
    Rule('~function_call~',
         ct(['System.out.println', '(', '~function_call_params~', ')']),
         FunctionCallDGN,
         has_params=True,
         name='System.out.println'
         ),
    Rule('~function_call~',
         ct(['System.out.print', '(', '~function_call_params~', ')']),
         FunctionCallDGN,
         has_params=True,
         name='System.out.print'
         ),
    Rule('~function_call~',
         ct(['Math.max', '(', '~function_call_params~', ')']),
         FunctionCallDGN,
         has_params=True,
         name='Math.max'
         ),
    Rule('~function_call~',
         ct(['Math.min', '(', '~function_call_params~', ')']),
         FunctionCallDGN,
         has_params=True,
         name='Math.min'
         ),

    Rule('~function_call_params~',
         ['~expression~'],
         FunctionCallParamsDGN,
         is_multiple=False),
    Rule('~function_call_params~',
         ct(['~expression~', ',', '~function_call_params~']),
         FunctionCallParamsDGN,
         is_multiple=True
         ),

    Rule('~cycle~',
         ct(['while', '(', '~logical_expression~', ')', '{', '~code_field~', '}']),
         WhileDGN,
         has_body=True),
    Rule('~cycle~',
         ct(['do', '{', '~code_field~', '}', 'while', '(', '~logical_expression~', ')', ';']),
         DoWhileDGN,
         has_body=True
         ),
    Rule('~cycle~',
         ct(['for', '(', '~var_declaration~', ';', '~logical_expression~', ';', '~assignment~', ')' ,'{', '~code_field~',
             '}']),
         ForDGN,
         is_initialization=True,
         has_body=True
         ),
    Rule('~cycle~',
         ct(['for', '(', '~assignment~', ';', '~logical_expression~', ';', '~assignment~', ')' ,'{', '~code_field~',
             '}']),
         ForDGN,
         is_initialization=False,
         has_body=True
         ),
    Rule('~cycle~',
         ct(['while', '(', '~logical_expression~', ')', '{', '}']),
         WhileDGN,
         has_body=True
         ),
    Rule('~cycle~',
         ct(['do', '{', '}', 'while', '(', '~logical_expression~', ')', ';']),
         DoWhileDGN,
         has_body=True
         ),
    Rule('~cycle~',
         ct(['for', '(', '~var_declaration~', ';', '~logical_expression~', ';', '~assignment~', ')', '{',
             '}']),
         ForDGN,
         is_initialization=True,
         has_body=False
         ),
    Rule('~cycle~',
         ct(['for', '(', '~assignment~', ';', '~logical_expression~', ';', '~assignment~', ')' ,'{',
             '}']),
         ForDGN,
         is_initialization=False,
         has_body=False
         ),

    Rule('~string_literal~',
         ['"', '~string_letters~', '"'],
         StringLiteralDGN,
         is_not_empty=True),
    Rule('~string_literal~',
         ['"', '"'],
         StringLiteralDGN,
         is_not_empty=False
         ),

    Rule('~string_letters~',
         ['~letter~', '~string_letters~'],
         StringLettersDGN,
         is_multiple=True),
    Rule('~string_letters~',
         ['~digit~', '~string_letters~'],
         StringLettersDGN,
         is_multiple=True
         ),
    Rule('~string_letters~',
         ['~other_symb~', '~string_letters~'],
         StringLettersDGN,
         is_multiple=True
         ),
    Rule('~string_letters~',
         ['~letter~'],
         StringLettersDGN,
         is_multiple=False
         ),
    Rule('~string_letters~',
         ['~digit~'],
         StringLettersDGN,
         is_multiple=False
         ),
    Rule('~string_letters~',
         ['~other_symb~'],
         StringLettersDGN,
         is_multiple=False
         ),
]
