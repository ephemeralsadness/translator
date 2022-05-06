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
        if x == ' ':
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
         has_functions=False),
    Rule('~program~',
         ct(['class', '~identifier~', '{', '~functions_declaration~', '~main_function~', '}']),
         ProgramDGN,
         has_functions=True),

    Rule('~identifier~',
         ['~letter~'],
         IdentifierDGN,
         is_one_letter=True),
    Rule('~identifier~',
         ['~letter~', '~identifier_next~'],
         IdentifierDGN,
         is_one_letter=False),

    *[
        Rule('~letter~',
             [i],
             LetterDGN,
             )
        for i in LETTERS
    ],

    Rule('~identifier_next~',
         ['~letter~', '~identifier_next~'],
         IdentifierNextDGN,
         starts_with_digit=False,
         is_multiple=True),
    Rule('~identifier_next~',
         ['~digit~', '~identifier_next~'],
         IdentifierNextDGN,
         starts_with_digit=True,
         is_multiple=True
         ),
    Rule('~identifier_next~',
         ['~letter~'],
         IdentifierNextDGN,
         starts_with_digit=False,
         is_multiple=False
         ),
    Rule('~identifier_next~',
         ['~digit~'],
         IdentifierNextDGN,
         starts_with_digit=True,
         is_multiple=False
         ),

    *[
        Rule('~digit~',
             [str(i)],
             DigitDGN)
        for i in range(0, 10)
    ],

    Rule('~main_function~',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '~code_field~', '}']),
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
         is_multiple=True),
    Rule('~code_field~',
         ct(['~instruction~']),
         CodeFieldDGN,
         is_multiple=False
         ),

    *[
        Rule('~instruction~',
             ct([f'~{what}~', ';']),
             InstructionDGN,
             what=what)
        for what in ['assignment', 'var_declaration', 'function_call', 'expression', 'cycle',
                     'if_operator', 'function_return', 'array1_initialization', 'array2_initialization',
                     'array1_element_assignment', 'array2_element_assignment', 'arraylist_initialization',
                     'arraylist_add', 'arraylist_clear', 'arraylist_remove']
    ],

    Rule('~assignment~',
         ct(['~identifier~', '~operator_assignment~', '~expression~']),
         AssignmentDGN),

    *[
        Rule('~operator_assignment~',
             ct([i]),
             OperatorAssignmentDGN)
        for i in ASSIGNMENT_OPERATORS
    ],

    *[
        Rule('~expression~',
             ct([f'~{what}~']),
             ExpressionDGN,
             what=what)
        for what in ['logical_expression', 'math_expression', 'symb_value', 'identifier',
                     'array1_element', 'array2_element', 'function_call', 'string_literal',
                     'arraylist_get']
    ],

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
    Rule('~logical_expression~',
         ct(['~arraylist_contains~']),
         LogicalExpressionDGN,
         what='arraylist_contains'
         ),
    Rule('~logical_expression~',
         ct(['~arraylist_is_empty~']),
         LogicalExpressionDGN,
         what='arraylist_is_empty'
         ),

    *[
        Rule('~math_expression~',
             [f'~{what}~'],
             MathExpressionDGN,
             what=what)
        for what in ['number', 'identifier', 'array1_element', 'array2_element',
                     'function_call', 'arraylist_size']
    ],
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
         is_multiple=True),
    Rule('~integer~',
         ['~digit~'],
         IntegerDGN,
         is_multiple=False
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

    *[
        Rule('~symb_value~',
            ["'", f'~f{what}~', "'"],
            SymbValueDGN)
        for what in ['letter', 'digit', 'other_symb']
    ],

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
             '(', '~function_params~', ')', '{', '~code_field~', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=True,
         has_body=True),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', '~function_params~', ')', '{', '~code_field~', '}']),
         FunctionsDeclarationDGN,
         multiple_declarations=False,
         has_params=True,
         has_body=True
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '~code_field~', '}', '~functions_declaration~']),
         FunctionsDeclarationDGN,
         multiple_declarations=True,
         has_params=False,
         has_body=True
         ),
    Rule('~functions_declaration~',
         ct(['static', '~function_return_type~', '~identifier~',
             '(', ')', '{', '~code_field~', '}']),
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
         ['void'],
         FunctionReturnTypeDGN,
         is_void=True
         ),

    *[
        Rule('~type~',
             ct([i]),
             TypeDGN)
        for i in VARIABLE_TYPES
    ],

    Rule('~function_params~',
         ct(['~type~', '~identifier~']),
         FunctionParamsDGN,
         is_multiple=False),
    Rule('~function_params~',
         ct(['~type~', '~identifier~', ',', '~function_params~']),
         FunctionParamsDGN,
         is_multiple=True
         ),

    Rule('~function_return~',
         ct(['return', '~expression~']),
         FunctionReturnDGN),

    Rule('~var_declaration~',
         ct(['~type~', '~identifier~']),
         VarDeclarationDGN,
         is_init=False),
    Rule('~var_declaration~',
         ct(['~type~', '~identifier~', '=', '~expression~']),
         VarDeclarationDGN,
         is_init=True
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

    # new rules
    Rule('~array1_initialization~',
         ct(['~type~', '[', ']', '~identifier~', '=',
             'new', '~type~', '[', '~math_expression~', ']']),
         Array1InitializationDGN),
    Rule('~array2_initialization~',
         ct(['~type~', '[', ']', '[', ']', '~identifier~', '=',
             'new', '~type~', '[', '~math_expression~', ']', '[', '~math_expression~', ']']),
         Array2InitializationDGN),
    Rule('~array1_element_assignment~',
         ct(['~array1_element~', '~operator_assignment~', '~expression~']),
         Array1ElementAssignmentDGN),
    Rule('~array2_element_assignment~',
         ct(['~array2_element~', '~operator_assignment~', '~expression~']),
         Array2ElementAssignmentDGN),
    Rule('~array1_element~',
         ct(['~identifier~', '[', '~math_expression~', ']']),
         Array1ElementDGN),
    Rule('~array2_element~',
         ct(['~identifier~', '[', '~math_expression~', ']', '[', '~math_expression~', ']']),
         Array2ElementDGN),
    *[
        Rule('~arraylist_initialization~',
             ct(['Arraylist', '<', wrapper_type, '>', '~identifier~', '=',
                 'new', 'Arraylist', '<', wrapper_type, '>', '(', ')']),
             ArraylistInitializationDGN,
             cpp_type=cpp_type)
        for wrapper_type, cpp_type in WRAPPER_TYPES_MAPPING.items()
    ],

    Rule('~arraylist_add~',
         ['~identifier~'] + ct(['.add', '(', '~expression~', ')']),
         ArraylistAddDGN),
    Rule('~arraylist_clear~',
         ['~identifier~'] + ct(['.clear', '(', ')']),
         ArraylistClearDGN),
    Rule('~arraylist_remove~',
         ['~identifier~'] + ct(['.remove', '(', '~math_expression~', ')']),
         ArraylistRemoveDGN),
    Rule('~arraylist_get~',
         ['~identifier~'] + ct(['.get', '(', '~math_expression~', ')']),
         ArraylistGetDGN),
    Rule('~arraylist_size~',
         ['~identifier~'] + ct(['.size', '(', ')']),
         ArraylistSizeDGN),
    Rule('~arraylist_contains~',
         ['~identifier~'] + ct(['.contains', '(', '~expression~', ')']),
         ArraylistContainsDGN),
    Rule('~arraylist_is_empty~',
         ['~identifier~'] + ct(['.isEmpty', '(', ')']),
         ArraylistIsEmptyDGN),
]
