from translator.syntax_analyzer.tree import rule_manager
from translator.code_generator.code_generator import generator_manager
from translator.semantic_analyzer.context_manager import context_manager

from translator.constants import KEYWORDS


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
        if self.functions:
            self.functions_declarations.check()
        self.main_function.check()

    def generate(self):
        generator_manager.println('#include <iostream>')
        generator_manager.println('#include <algorithm>')
        generator_manager.println('#include <string>')
        generator_manager.println()
        if self.functions:
            self.functions_declarations.generate()
        self.main_function.generate()


class IdentifierDGN(DGN):
    def __init__(self, is_one_letter):
        super().__init__()
        self.is_one_letter = is_one_letter
        if not self.is_one_letter:
            self.identifier_next = rule_manager.create_next_rule_instance()
        self.identifier_start = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        var_type, is_init = context_manager.type_of_variable(self.reduce())
        if self.reduce() in KEYWORDS:
            raise Exception('Wrong variable name: reserved keyword "{}"'.format(self.reduce()))
        if var_type is None:
            raise Exception('Variable "{}" has not been declared'.format(self.reduce()))
        if not is_init:
            raise Exception('Variable "{}" has not been initialized before using'.format(var_type))

    def generate(self):
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
        self.value = memo
        return self.value

    def type(self):
        var_type, is_init = context_manager.type_of_variable(self.reduce())
        return 'number' if var_type in ['float', 'double', 'int'] else var_type


class IdentifierStartDGN(DGN):
    def __init__(self):
        super().__init__()
        self.letter_instance = rule_manager.create_next_rule_instance()

    def check(self):
        pass

    def generate(self):
        pass


class LetterDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

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
            return self.symbol.letter_instance.value
        return self.symbol.letter_instance.value + self.next.reduce()


class DigitDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        pass


class MainFunctionDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.has_body = has_body
        if self.has_body:
            self.function_body = rule_manager.create_next_rule_instance()

    def check(self):
        if self.has_body:
            context_manager.push_scope()
            self.function_body.check()
            context_manager.pop_scope()

    def generate(self):
        generator_manager.println('int main() {')
        generator_manager.increase_tabs()
        if self.has_body:
            self.function_body.generate()
        generator_manager.println()
        generator_manager.println('return 0;')
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class CodeFieldDGN(DGN):
    def __init__(self, has_code_field):
        super().__init__()
        self.has_code_field = has_code_field
        if self.has_code_field:
            self.code_field = rule_manager.create_next_rule_instance()
        self.instruction = rule_manager.create_next_rule_instance()

    def check(self):
        self.instruction.check()
        if self.has_code_field:
            self.code_field.check()

    def generate(self):
        self.instruction.generate()
        generator_manager.println()
        if self.has_code_field:
            self.code_field.generate()


class InstructionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.concrete_instruction = rule_manager.create_next_rule_instance()

    def check(self):
        self.concrete_instruction.check()

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
        idx = self.identifier.reduce()
        var_type, is_init = context_manager.type_of_variable(idx)
        if var_type is None:
            raise Exception('Cannot assign value to undeclared variable "{}"'.format(idx))
        # expression_type = self.expression.type()
        # if var_type not in self.expression.type():
        #     raise Exception('Cannot assign value to variable "{}": wrong types {} and {}'.format(
        #         idx, var_type, expression_type
        #     ))
        self.expression.check()

    def generate(self):
        self.identifier.generate()
        generator_manager.print(' ')
        self.assignment_operator.generate()
        generator_manager.print(' ')
        self.expression.generate()


class OperatorAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.operator)


class ExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()

    def generate(self):
        self.expression.generate()

    def type(self):
        return self.expression.type()


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
        if self.what in ['math_comparison', 'symb_comparison', '&&', '||']:
            self.lhs.check()
            self.rhs.check()
        if self.what == 'boolean_value':
            self.boolean_value.check()
        if self.what == 'braced':
            self.expression.check()

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

    def type(self):
        return 'boolean'


class MathExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what

        if self.what in ['+', '-', '*', '/', '%']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = rule_manager.create_next_rule_instance()
            self.lhs = rule_manager.create_next_rule_instance()
        else:
            self.value = rule_manager.create_next_rule_instance()

    def check(self):
        # todo check math expression identifiers to be numbers
        if self.what in ['+', '-', '*', '/', '%']:
            self.lhs.check()
            self.rhs.check()
        else:
            self.value.check()

    def generate(self):
        if self.what in ['+', '-', '*', '/', '%']:
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

    def type(self):
        return 'number'


class AdditionSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.operator)


class MultiplicationSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.operator)


class NumberDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance()

    def check(self):
        pass

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
        pass

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
        pass

    def generate(self):
        self.value = self.reduce()

    def reduce(self):
        if self.value is not None:
            return self.value
        self.value = self.lhs.generate() + '.' + self.rhs.generate()


class CompareOperatorDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.operator)


class SymbValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        pass

    def generate(self):
        generator_manager.print('\'')
        generator_manager.print(self.symbol.value)
        generator_manager.print('\'')

    def type(self):
        return 'char'


class OtherSymbDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        pass


class IfOperatorDGN(DGN):
    def __init__(self, what, has_empty_if_body=None, has_empty_else_body=None):
        super().__init__()
        self.what = what
        self.has_empty_if_body = has_empty_if_body
        self.has_empty_else_body = has_empty_else_body

        if self.what == 'if-else' and (not self.has_empty_else_body):
            self.else_code_field = rule_manager.create_next_rule_instance()
        if self.what == 'if-else-if':
            self.else_if = rule_manager.create_next_rule_instance()

        if not self.has_empty_if_body:
            self.if_code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        if not self.has_empty_if_body:
            context_manager.push_scope()
            self.if_code_field.check()
            context_manager.pop_scope()
        if self.what == 'if-else' and (not self.has_empty_else_body):
            context_manager.push_scope()
            self.else_code_field.check()
            context_manager.pop_scope()
        if self.what == 'if-else-if':
            self.else_if.check()

    def generate(self):
        generator_manager.print('if (')
        self.expression.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        if not self.has_empty_if_body:
            self.if_code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.print('}')

        if self.what == 'if-else-if':
            generator_manager.print(' else ')
            self.else_if.generate()
        elif self.what == 'if-else':
            generator_manager.println(' else {')
            generator_manager.increase_tabs()
            if not self.has_empty_else_body:
                self.else_code_field.generate()
            generator_manager.decrease_tabs()
            generator_manager.print('}')


class BooleanValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.symbol)


class FunctionsDeclarationDGN(DGN):
    def __init__(self, multiple_declarations, has_params, has_body):
        super().__init__()
        self.multiple_declarations = multiple_declarations
        self.has_params = has_params
        self.has_body = has_body
        if self.multiple_declarations:
            self.function_declarations = rule_manager.create_next_rule_instance()
        if self.has_body:
            self.function_body = rule_manager.create_next_rule_instance()
        if self.has_params:
            self.function_params = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()
        self.function_return_type = rule_manager.create_next_rule_instance()

    def check(self):
        # todo check if function returns correct type expression
        # todo add to current scope function params
        if self.multiple_declarations:
            self.function_declarations.check()
        if self.has_body:
            context_manager.push_scope()
            if self.has_params:
                pass
            self.function_body.check()
            context_manager.pop_scope()


    def generate(self):
        generator_manager.print('static ')
        self.function_return_type.generate()
        generator_manager.print(' ')
        self.identifier.generate()
        generator_manager.print('(')
        if self.has_params:
            self.function_params.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        if self.has_body:
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
        pass

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
        pass

    def generate(self):
        generator_manager.print(self.reduce())

    def reduce(self):
        if self.value is not None:
            return self.value
        self.value = self.valuable_type.value


class ValuableTypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        if self.value == 'boolean':
            generator_manager.print('bool')
        else:
            generator_manager.print(self.value)


class FunctionParamsDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.is_multiple = is_multiple

        if is_multiple:
            self.function_params = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()
        self.valuable_type = rule_manager.create_next_rule_instance()
        self.value = None

    def check(self):
        context_manager.set_type_of_variable(self.identifier.reduce(), self.valuable_type.value, True)
        if self.is_multiple:
            self.function_params.check()

    def generate(self):
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
        self.code_field.check()

    def generate(self):
        self.code_field.generate()


class FunctionReturnDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        pass

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
        var_type, is_init = context_manager.type_of_variable(self.identifier.reduce())
        if var_type is not None:
            raise Exception('Multiple declaration of variable "{}"'.format(self.identifier.reduce()))
        context_manager.set_type_of_variable(self.identifier.reduce(), self.valuable_type.value, self.is_initialized)

    def generate(self):
        self.valuable_type.generate()
        generator_manager.print(' ')
        self.identifier.generate()
        if self.is_initialized:
            generator_manager.print(' = ')
            self.expression.generate()


class FunctionCallDGN(DGN):
    def __init__(self, has_params, name=None):
        super().__init__()
        self.has_params = has_params
        self.name = name
        if self.has_params:
            self.function_call_params = rule_manager.create_next_rule_instance()
        if self.name is None:
            self.function_identifier = rule_manager.create_next_rule_instance()

    def check(self):
        if self.has_params:
            self.function_call_params.check()
        if self.name is None:
            self.function_identifier.check()
        # todo check params to function signature

    def generate(self):
        if self.name is not None:
            if self.name == 'System.out.print':
                generator_manager.print('std::cout << ')
                if self.has_params:
                    self.function_call_params.generate()
            elif self.name == 'System.out.println':
                generator_manager.print('std::cout << ')
                if self.has_params:
                    self.function_call_params.generate()
                generator_manager.print(' << std::endl')
            elif self.name == 'Math.max':
                generator_manager.print('std::max(')
                if self.has_params:
                    self.function_call_params.generate()
                generator_manager.print(')')
            elif self.name == 'Math.min':
                generator_manager.print('std::min(')
                if self.has_params:
                    self.function_call_params.generate()
                generator_manager.print(')')
        else:
            self.function_identifier.generate()
            generator_manager.print('(')
            if self.has_params:
                self.function_call_params.generate()
            generator_manager.print(')')

    def type(self):
        return context_manager.get_function_return_type()


class FunctionCallParamsDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.is_multiple = is_multiple
        if is_multiple:
            self.function_call_params = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        if self.is_multiple:
            self.function_call_params.check()
        self.expression.check()
        # todo check all expr are declared

    def generate(self):
        self.expression.generate()
        if self.is_multiple:
            generator_manager.print(', ')
            self.function_call_params.generate()


class WhileDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.has_body = has_body
        if self.has_body:
            self.code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        context_manager.push_scope()
        if self.has_body:
            self.code_field.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.print('while (')
        self.expression.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        if self.has_body:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class DoWhileDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.has_body = has_body
        self.expression = rule_manager.create_next_rule_instance()
        if self.has_body:
            self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        context_manager.push_scope()
        if self.has_body:
            self.code_field.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.print('do {')
        generator_manager.increase_tabs()
        if self.has_body:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.print('} while (')
        self.expression.generate()
        generator_manager.println(')')


class ForDGN(DGN):
    def __init__(self, is_initialization, has_body):
        super().__init__()
        self.has_body = has_body
        self.is_initialization = is_initialization
        if self.has_body:
            self.code_field = rule_manager.create_next_rule_instance()
        self.move_assignment = rule_manager.create_next_rule_instance()
        self.logical_expression = rule_manager.create_next_rule_instance()
        self.assignment = rule_manager.create_next_rule_instance()

    def check(self):
        context_manager.push_scope()
        self.move_assignment.check()
        self.logical_expression.check()
        self.assignment.check()
        if self.has_body:
            self.code_field.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.print('for (')
        self.assignment.generate()
        generator_manager.print('; ')
        self.logical_expression.generate()
        generator_manager.print('; ')
        self.move_assignment.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        if self.has_body:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class StringLiteralDGN(DGN):
    def __init__(self, is_not_empty):
        super().__init__()
        self.is_not_empty = is_not_empty
        if self.is_not_empty:
            self.letters = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print('"')
        if self.is_not_empty:
            self.letters.generate()
        generator_manager.print('"')


class StringLettersDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.is_multiple = is_multiple
        if self.is_multiple:
            self.string_letters = rule_manager.create_next_rule_instance()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        generator_manager.print(self.symbol.value)
        if self.is_multiple:
            self.string_letters.generate()

