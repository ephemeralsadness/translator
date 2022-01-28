from translator.syntax_analyzer.tree import rule_manager
from translator.code_generator.code_generator import generator_manager


class DGN:
    def __init__(self):
        ...

    def check(self):
        ...

    def generate(self):
        ...


class ProgramDGN(DGN):
    def __init__(self, functions):
        super().__init__()
        self.functions = functions
        self.main_function = rule_manager.create_next_rule_instance()
        self.functions_declarations = None
        if self.functions:
            self.functions_declarations = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.println('#include <iostream>')
        generator_manager.println('#include <algorithm>')
        generator_manager.println('#include <string>')
        generator_manager.println()
        if self.functions:
            self.functions_declarations.generate()
        self.main_function.generate()
        generator_manager.println()


class IdentifierDGN(DGN):
    def __init__(self, is_one_letter):
        super().__init__()
        self.is_one_letter = is_one_letter
        if not self.is_one_letter:
            self.identifier_next = rule_manager.create_next_rule_instance()
        self.identifier_start = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        if self.value is None:
            self.value = self.reduce()
        generator_manager.print(self.value)

    def reduce(self):
        if self.value is not None:
            return self.value
        memo = None
        if self.is_one_letter:
            memo = self.identifier_start.letter_instance.value
        else:
            memo = self.identifier_start.letter_instance.value + self.identifier_next.reduce()
        self.identifier_start = None
        self.identifier_next = None
        return memo


class IdentifierStartDGN(DGN):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.letter_instance = rule_manager.create_next_rule_instance()

    def check(self):
        pass

    def generate(self):
        pass


class LetterDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        pass

    def generate(self):
        pass


class IdentifierNextDGN(DGN):
    def __init__(self, is_digit, is_one_letter):
        super().__init__()
        self.is_one_letter = is_one_letter
        self.is_digit = is_digit
        self.next = None
        if not self.is_one_letter:
            self.next = rule_manager.create_next_rule_instance()
            self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        pass

    def generate(self):
        pass

    def reduce(self):
        if self.is_one_letter:
            return self.symbol.value
        return self.symbol.value + self.next.reduce()


class DigitDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        pass

    def generate(self):
        pass


class MainFunctionDGN(DGN):
    def __init__(self):
        super().__init__()
        self.function_body = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.println('int main() {')
        generator_manager.increase_tabs()
        self.function_body.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class CodeFieldDGN(DGN):
    def __init__(self, is_lambda):
        super().__init__()
        self.is_lambda = is_lambda
        self.code_field = None
        if not self.is_lambda:
            self.code_field = rule_manager.create_next_rule_instance()
            self.instruction = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if not self.is_lambda:
            self.instruction.generate()
            generator_manager.println()
            self.code_field.generate()


class InstructionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.concrete_instruction = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.concrete_instruction.generate()
        if self.what not in ['cycle', 'if_operator']:
            generator_manager.print(';')


class AssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.assignment_operator = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.identifier.generate()
        generator_manager.print(' ')
        self.assignment_operator.generate()
        generator_manager.print(' ')
        self.expression.generate()


class OperatorAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.operator)


class ExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.expression.generate()


class LogicalExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        if self.what in ['math_comparison', 'symb_comparison']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = rule_manager.create_next_rule_instance()
            self.lhs = rule_manager.create_next_rule_instance()
        if self.what == 'boolean_value':
            self.boolean_value = rule_manager.create_next_rule_instance()
        if self.what == 'braced':
            self.expression = rule_manager.create_next_rule_instance()
        if self.what in ['&&', '||']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.lhs = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if self.what in ['math_comparison', 'symb_comparison']:
            self.lhs.generate()
            generator_manager.print(' ')
            self.operator.generate()
            generator_manager.print(' ')
            self.rhs.generate()
        if self.what == 'boolean_value':
            self.boolean_value.generate()
        if self.what == 'braced':
            generator_manager.print('(')
            self.expression.generate()
            generator_manager.print(')')
        if self.what in ['&&', '||']:
            self.lhs.generate()
            generator_manager.print(' ' + self.what + ' ')
            self.rhs.generate()


class MathExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what

        if self.what in ['+', '-']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = rule_manager.create_next_rule_instance()
            self.lhs = rule_manager.create_next_rule_instance()
        else:
            self.value = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if self.what in ['+', '-']:
            self.lhs.generate()
            generator_manager.print(' ')
            self.operator.generate()
            generator_manager.print(' ')
            self.rhs.generate()
        elif self.what == 'unary_minus':
            generator_manager.print('-')
            self.value.generate()
        elif self.what == 'braced':
            generator_manager.print('(')
            self.value.generate()
            generator_manager.print(')')
        else:
            self.value.generate()


class AdditionSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.operator)


class MultiplicationSignDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.operator)


class NumberDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.value.generate()


class IntegerDGN(DGN):
    def __init__(self, is_one_digit):
        super().__init__()
        self.is_one_digit = is_one_digit
        if not self.is_one_digit:
            self.integer = rule_manager.create_next_rule_instance()
        self.digit = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        self.value = self.reduce()
        generator_manager.print(self.value)

    def reduce(self):
        if self.value is not None:
            return self.value
        if self.is_one_digit:
            return self.digit.value
        return self.digit.value + self.integer.reduce()


class RealNumberDGN(DGN):
    def __init__(self):
        super().__init__()
        self.rhs = rule_manager.create_next_rule_instance()
        self.lhs = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        self.value = self.reduce()

    def reduce(self):
        if self.value is not None:
            return self.value
        self.value = self.lhs.generate() + '.' + self.rhs.generate()


class CompareOperatorDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.operator)


class SymbValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('\'')
        generator_manager.print(self.symbol.value)
        generator_manager.print('\'')


class OtherSymbDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        pass

    def generate(self):
        pass


class IfOperatorDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        if self.what == 'if-else':
            self.else_code_field = rule_manager.create_next_rule_instance()
        if self.what == 'if-else-if':
            self.else_if = rule_manager.create_next_rule_instance()
        self.if_code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('if (')
        self.expression.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        self.if_code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.print('}')

        if self.what == 'if-else-if':
            generator_manager.print(' else ')
            self.else_if.generate()
        elif self.what == 'if-else':
            generator_manager.println(' else {')
            generator_manager.increase_tabs()
            self.else_code_field.generate()
            generator_manager.decrease_tabs()
            generator_manager.print('}')


class BooleanValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.symbol)


class FunctionsDeclarationDGN(DGN):
    def __init__(self, multiple_declarations):
        super().__init__()
        self.multiple_declarations = multiple_declarations
        if self.multiple_declarations:
            self.function_declarations = rule_manager.create_next_rule_instance()
        self.function_body = rule_manager.create_next_rule_instance()
        self.function_params = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()
        self.function_return_type = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('static ')
        self.function_return_type.generate()
        generator_manager.print(' ')
        self.identifier.generate()
        generator_manager.print('(')
        self.function_params.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        self.function_body.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')
        generator_manager.println()
        generator_manager.println()
        if self.multiple_declarations:
            self.function_declarations.generate()


class FunctionReturnTypeDGN(DGN):
    def __init__(self, is_void):
        super().__init__()
        self.is_void = is_void
        if not self.is_void:
            self.return_type = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.reduce())

    def reduce(self):
        if self.value is not None:
            return self.value
        self.value = ('void' if self.is_void else self.return_type.reduce())


class TypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.valuable_type = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.reduce())

    def reduce(self):
        if self.value is not None:
            return self.value
        self.value = self.valuable_type.value


class ValuableTypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.value)


class FunctionParamsDGN(DGN):
    def __init__(self, is_lambda, is_multiple):
        super().__init__()
        self.is_lambda = is_lambda
        self.is_multiple = is_multiple

        if is_multiple:
            self.function_params = rule_manager.create_next_rule_instance()

        if not is_lambda:
            self.identifier = rule_manager.create_next_rule_instance()
            self.valuable_type = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        ...

    def generate(self):
        if self.is_lambda:
            return

        self.valuable_type.generate()
        generator_manager.print(' ')
        self.identifier.generate()

        if self.is_multiple:
            generator_manager.print(', ')
            self.function_params.generate()

    def reduce(self):
        ...


class FunctionBodyDGN(DGN):
    def __init__(self):
        super().__init__()
        self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.code_field.generate()


class FunctionReturnDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.println('return ')
        self.expression.generate()


class VarDeclarationDGN(DGN):
    def __init__(self, is_initialized):
        super().__init__()
        self.is_initialized = is_initialized
        if is_initialized:
            self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()
        self.valuable_type = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        self.valuable_type.generate()
        generator_manager.print(' ')
        self.identifier.generate()
        if self.is_initialized:
            generator_manager.print(' = ')
            self.expression.generate()


class FunctionCallDGN(DGN):
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.function_call_params = rule_manager.create_next_rule_instance()
        if self.name is None:
            self.function_identifier = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if self.name is not None:
            generator_manager.print(self.name)
        else:
            self.function_identifier.generate()
        generator_manager.print('(')
        self.function_call_params.generate()
        generator_manager.print(')')


class FunctionCallParamsDGN(DGN):
    def __init__(self, is_lambda, is_multiple):
        super().__init__()
        self.is_lambda = is_lambda
        self.is_multiple = is_multiple

        if is_multiple:
            self.function_call_params = rule_manager.create_next_rule_instance()

        if not is_lambda:
            self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if self.is_lambda:
            return
        self.expression.generate()
        if self.is_multiple:
            generator_manager.print(', ')
            self.function_call_params.generate()


class WhileDGN(DGN):
    def __init__(self):
        super().__init__()
        self.code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('while (')
        self.expression.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class DoWhileDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('do {')
        generator_manager.increase_tabs()
        self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.print('} while (')
        self.expression.generate()
        generator_manager.println(')')


class ForDGN(DGN):
    def __init__(self, is_initialization):
        super().__init__()
        self.is_initialization = is_initialization
        self.code_field = rule_manager.create_next_rule_instance()
        self.move_assignment = rule_manager.create_next_rule_instance()
        self.logical_expression = rule_manager.create_next_rule_instance()
        self.assignment = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('for (')
        self.assignment.generate()
        generator_manager.print('; ')
        self.logical_expression.generate()
        generator_manager.print('; ')
        self.move_assignment.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class StringLiteralDGN(DGN):
    def __init__(self):
        super().__init__()
        self.letters = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('"')
        self.letters.generate()
        generator_manager.print('"')


class StringLettersDGN(DGN):
    def __init__(self, is_lambda):
        super().__init__()
        self.is_lambda = is_lambda
        if not self.is_lambda:
            self.string_letters = rule_manager.create_next_rule_instance()
            self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        if self.is_lambda:
            return
        generator_manager.print(self.symbol.value)
        self.string_letters.generate()

