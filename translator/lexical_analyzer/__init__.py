from translator.lexical_analyzer.token_machine import Symbols, State, token_machine, classify_symbol


class LexicalAnalyzer:

    def __init__(self):
        ...

    def run(self, java_code: str) -> list[str]:
        tokens = []
        current_token = ''
        state = State.NORMAL
        for c in java_code:
            new_state, finalize_value = token_machine[state.value[0]][classify_symbol(c).value[0]]

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
                raise Exception('Unexpected symbol: {}'.format(c))

        if current_token != '':
            tokens.append(current_token)

        return tokens

