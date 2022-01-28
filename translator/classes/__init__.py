from translator.syntax_analyzer.tree import rule_manager


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
        ...


class IdentifierDGN(DGN):
    def __init__(self, is_one_letter):
        super().__init__()
        self.is_one_letter = is_one_letter
        if not self.is_one_letter:
            self.identifier_next = rule_manager.create_next_rule_instance()
        self.identifier_start = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class IdentifierStartDGN(DGN):
    def __init__(self, letter):
        super().__init__()
        self.letter = letter
        self.letter_instance = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class LetterDGN(DGN):
    def __init__(self):
        super().__init__()
        self.letter = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class IdentifierNextDGN(DGN):
    def __init__(self, is_digit, has_next):
        super().__init__()
        self.is_digit = is_digit
        self.has_next = has_next
        self.next = None
        if self.has_next:
            self.next = rule_manager.create_next_rule_instance()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class DigitDGN(DGN):
    def __init__(self):
        super().__init__()
        self.digit = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class MainFunctionDGN(DGN):
    def __init__(self):
        super().__init__()
        self.function_body = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


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
        ...


class InstructionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.concrete_instruction = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class AssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.assignment_operator = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class OperatorAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class ExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


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
        ...


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
        ...


class AdditionSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class MultiplicationSignDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class NumberDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class IntegerDGN(DGN):
    def __init__(self, is_one_digit):
        super().__init__()
        self.is_one_digit = is_one_digit
        if not self.is_one_digit:
            self.integer = rule_manager.create_next_rule_instance()
        self.digit = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class RealNumberDGN(DGN):
    def __init__(self):
        super().__init__()
        self.rhs = rule_manager.create_next_rule_instance()
        self.lhs = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class CompareOperatorDGN(DGN):
    def __init__(self):
        super().__init__()
        self.operator = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


class SymbValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class SymbValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


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
        ...


class BooleanValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.symbol = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


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
        ...


class FunctionReturnTypeDGN(DGN):
    def __init__(self, is_void):
        super().__init__()
        self.is_void = is_void
        if not self.is_void:
            self.return_type = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class TypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.valuable_type = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class ValuableTypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        ...

    def generate(self):
        ...


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

    def check(self):
        ...

    def generate(self):
        ...


class FunctionBodyDGN(DGN):
    def __init__(self):
        super().__init__()
        self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class FunctionReturnDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class VarDeclarationDGN(DGN):
    def __init__(self, is_initialized):
        super().__init__()
        if is_initialized:
            self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()
        self.valuable_type = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


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
        ...


class WhileDGN(DGN):
    def __init__(self):
        super().__init__()
        self.code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class DoWhileDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class ForDGN(DGN):
    def __init__(self, is_initialization):
        super().__init__()
        self.code_field = rule_manager.create_next_rule_instance()
        self.assignment = rule_manager.create_next_rule_instance()
        self.logical_expression = rule_manager.create_next_rule_instance()
        self.assignment = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class StringLiteralDGN(DGN):
    def __init__(self, is_empty):
        super().__init__()
        self.is_empty = is_empty
        if not self.is_empty:
            self.letters = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...


class StringLettersDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.is_multiple = is_multiple
        if is_multiple:
            self.string_letters = rule_manager.create_next_rule_instance()
        self.symbol = rule_manager.create_next_rule_instance()

    def check(self):
        ...

    def generate(self):
        ...