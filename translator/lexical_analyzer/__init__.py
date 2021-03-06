from translator.lexical_analyzer.token_machine import Symbols, State, token_machine, classify_symbol
import translator.constants as constants

class LexicalAnalyzer:

    def __init__(self):
        ...

    def run(self, java_code: str) -> list[str]:
        tokens = []
        current_token = ''
        state = State.NORMAL

        line_number = 1
        symbol_number = 1

        for c in java_code:
            new_state, finalize_value = token_machine[state.value][classify_symbol(c).value]
            if finalize_value == 0:
                ...
            elif finalize_value == 1:
                current_token += c
            elif finalize_value == 2:
                if current_token != '':
                    tokens.append(current_token)
                current_token = c if c not in Symbols.WHITESPACES else ''
            elif finalize_value == 3:
                current_token += c
                tokens.append(current_token)
                current_token = ''
            elif finalize_value == 4:
                tokens.append(current_token)
                tokens.append(c)
                current_token = ''
            state = new_state

            if state == State.ERROR:
                raise Exception(f'Unexpected symbol: {c} at line {line_number}, symbol {symbol_number}')

            if c == '\n':
                line_number += 1
                symbol_number = 1
            symbol_number += 1

        if current_token != '':
            tokens.append(current_token)

        if state == State.STRING_LITERAL:
            raise Exception('Expected end of string literal')
        if state == State.CHAR_LITERAL:
            raise Exception('Expected end of char literal')

        # post-check
        for token in tokens:
            if token[0] in Symbols.OPERATORS and token not in constants.OPERATORS:
                raise Exception(f'Bad operator: {token}')

        return tokens

