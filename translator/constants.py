import string

UNARY_OPERATORS = ['+', '-', '++', '--', '!']
ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '%']
LOGICAL_OPERATORS = ['||', '&&']
COMPARISON_OPERATORS = ['<', '>', '==', '!=', '<=', '>=']
ASSIGNMENT_OPERATORS = ['=', '+=', '-=', '*=', '/=', '%=']
LETTERS = list(string.ascii_letters)

OPERATORS = UNARY_OPERATORS + ARITHMETIC_OPERATORS + LOGICAL_OPERATORS + COMPARISON_OPERATORS + ASSIGNMENT_OPERATORS
