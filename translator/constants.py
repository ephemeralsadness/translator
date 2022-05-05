import string

UNARY_OPERATORS = ['+', '-', '++', '--', '!']
ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '%']
LOGICAL_OPERATORS = ['||', '&&']
COMPARISON_OPERATORS = ['<', '>', '==', '!=', '<=', '>=']
ASSIGNMENT_OPERATORS = ['=', '+=', '-=', '*=', '/=', '%=']
OTHER_SYMBOLS = ['!', '@', '#', '$', '%', '^', '&',
                 '*', '(', ')', '-', '+', ']', '[', '{',
                 '}', '№', ';', ':', '?', '=', '<', '>',
                 '.', ',', ' ']
WRAPPER_TYPES_MAPPING = {
    'Integer': 'int',
    'Byte': 'byte',
    'Short': 'short',
    'Long': 'long long',
    'Float': 'float',
    'Boolean': 'bool',
    'Double': 'double'
}
VARIABLE_TYPES = ['int', 'byte', 'short', 'long', 'float', 'char', 'boolean', 'double', 'String']
LETTERS = list(string.ascii_letters) + ['_']

OPERATORS = UNARY_OPERATORS + ARITHMETIC_OPERATORS + LOGICAL_OPERATORS + COMPARISON_OPERATORS + ASSIGNMENT_OPERATORS

KEYWORDS = VARIABLE_TYPES + 'class do else for if public return static while'.split(' ')
