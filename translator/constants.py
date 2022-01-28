import string

UNARY_OPERATORS = ['+', '-', '++', '--', '!']
ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '%']
LOGICAL_OPERATORS = ['||', '&&']
COMPARISON_OPERATORS = ['<', '>', '==', '!=', '<=', '>=']
ASSIGNMENT_OPERATORS = ['=', '+=', '-=', '*=', '/=', '%=']
OTHER_SYMBOLS = ['_', '!', '@', '#', '$', '%', '^', '&',
                 '*', '(', ')', '-', '+', ']', '[', '{',
                 '}', '№', ';', ':', '?', '=', '<', '>',
                 '.', ',', ' ']
VARIABLE_TYPES = ['int', 'float', 'char', 'boolean', 'double', 'String']
LETTERS = list(string.ascii_letters)

OPERATORS = UNARY_OPERATORS + ARITHMETIC_OPERATORS + LOGICAL_OPERATORS + COMPARISON_OPERATORS + ASSIGNMENT_OPERATORS

KEYWORDS = VARIABLE_TYPES + 'class do else for if public return static while'.split(' ')
