import string
from enum import Enum


class State(Enum):
    NORMAL = 0
    IDENTIFIER = 1
    NUMBER = 2
    OPERATOR = 3
    STRING_LITERAL = 4
    CHAR_LITERAL = 5
    ERROR = 6


class Symbol(Enum):
    DIGIT = 0
    WHITESPACE = 1
    LETTER = 2
    PARENTHESIS = 3
    OPERATOR = 4
    SEMICOLON = 5
    COMMA = 6
    STRING_QUOTE = 7
    CHAR_QUOTE = 8
    DOT = 9
    OTHER_SYMBOL = 10
    NON_GRAMMAR = 11


class Symbols:
    DIGITS = string.digits
    WHITESPACES = string.whitespace
    LETTERS = string.ascii_letters + '_'
    PARENTHESIS = '(){}[]'
    OPERATORS = '+-*/%><=!&|'
    SEMICOLONS = ';'
    COMMAS = ','
    STRING_QUOTES = '"'
    CHAR_QUOTES = '\''
    DOTS = '.'
    OTHER_SYMBOLS = '#@№$^:?'


def classify_symbol(c: str) -> Symbol:
    if c in Symbols.DIGITS:
        return Symbol.DIGIT
    elif c in Symbols.WHITESPACES:
        return Symbol.WHITESPACE
    elif c in Symbols.LETTERS:
        return Symbol.LETTER
    elif c in Symbols.PARENTHESIS:
        return Symbol.PARENTHESIS
    elif c in Symbols.OPERATORS:
        return Symbol.OPERATOR
    elif c in Symbols.SEMICOLONS:
        return Symbol.SEMICOLON
    elif c in Symbols.COMMAS:
        return Symbol.COMMA
    elif c in Symbols.STRING_QUOTES:
        return Symbol.STRING_QUOTE
    elif c in Symbols.CHAR_QUOTES:
        return Symbol.CHAR_QUOTE
    elif c in Symbols.DOTS:
        return Symbol.DOT
    elif c in Symbols.OTHER_SYMBOLS:
        return Symbol.OTHER_SYMBOL
    return Symbol.NON_GRAMMAR


token_machine = [
    # DIGIT, WHITESPACE, LETTER, PARENTHESIS, OPERATOR,
    # SEMICOLON, COMMA, STRING_QUOTE, CHAR_QUOTE, OTHER_SYMBOL

    # digit [0 - don't add, 1 - don't finalize, 2 - finalize previous, 3 - finalize now, 4 - finalize both]

    # State = NORMAL
    [(State.NUMBER, 1), (State.NORMAL, 0), (State.IDENTIFIER, 1), (State.NORMAL, 3),
     (State.OPERATOR, 1), (State.NORMAL, 3), (State.NORMAL, 3), (State.STRING_LITERAL, 1),
     (State.CHAR_LITERAL, 1), (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0)],
    # State = IDENTIFIER
    [(State.IDENTIFIER, 1), (State.NORMAL, 2), (State.IDENTIFIER, 1), (State.NORMAL, 4),
     (State.OPERATOR, 2), (State.NORMAL, 4), (State.NORMAL, 4), (State.ERROR, 0),
     (State.ERROR, 0), (State.IDENTIFIER, 1), (State.ERROR, 0), (State.ERROR, 0)],
    # State = NUMBER
    [(State.NUMBER, 1), (State.NORMAL, 2), (State.ERROR, 0), (State.NORMAL, 4),
     (State.NORMAL, 4), (State.NORMAL, 4), (State.NORMAL, 4), (State.ERROR, 0),
     (State.ERROR, 0), (State.NUMBER, 1), (State.ERROR, 0), (State.ERROR, 0)],
    # State = OPERATOR
    [(State.NUMBER, 2), (State.NORMAL, 2), (State.IDENTIFIER, 2), (State.NORMAL, 4),
     (State.OPERATOR, 1), (State.ERROR, 0), (State.ERROR, 0), (State.STRING_LITERAL, 2),
     (State.CHAR_LITERAL, 2), (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0)],
    # State = STRING_LITERAL
    [(State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1),
     (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.NORMAL, 3),
     (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.STRING_LITERAL, 1), (State.ERROR, 0)],
    # State = CHAR_LITERAL
    [(State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1),
     (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1),
     (State.NORMAL, 3), (State.CHAR_LITERAL, 1), (State.CHAR_LITERAL, 1), (State.ERROR, 0)],
    # State = ERROR
    [(State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0),
     (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0),
     (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0), (State.ERROR, 0)],
]


RESERVED_KEYWORDS = {
    'System.out.println',
    'Math.max',
    'Math.min',
    'int',
    'char',
    'float',
    'boolean',
    'if',
    'else',
    'while',
    'do',
    'for',
    'void',
    'main',
    'class',
    'public',
    'static',
    'return'
}