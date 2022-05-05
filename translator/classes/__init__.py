from translator.syntax_analyzer.tree import rule_manager
from translator.code_generator.code_generator import generator_manager
from translator.semantic_analyzer.context_manager import context_manager


class DGN:
    def __init__(self):
        ...

    def check(self):
        ...

    def generate(self):
        ...

    def type(self):
        return None


class ProgramDGN(DGN):
    def __init__(self, has_functions):
        super().__init__()
        self.main_function = rule_manager.create_next_rule_instance()

        has_functions = has_functions
        self.functions = None
        if has_functions:
            self.functions = rule_manager.create_next_rule_instance()

        self.class_name = rule_manager.create_next_rule_instance()

    def check(self):
        context_manager.push_scope()
        context_manager.create_variable(self.class_name, 'class_name', False)
        if self.functions is not None:
            self.functions.check()
        context_manager.push_scope()
        self.main_function.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.println('#include <iostream>')
        generator_manager.println('#include <algorithm>')
        generator_manager.println('#include <string>')
        generator_manager.println('#include <vector>')
        generator_manager.println()
        if self.functions is not None:
            self.functions.generate()
        self.main_function.generate()

    def type(self):
        return 'class_name'


class IdentifierDGN(DGN):
    def __init__(self, is_one_letter):
        super().__init__()
        is_one_letter = is_one_letter
        identifier_next = ''
        if not is_one_letter:
            identifier_next = rule_manager.create_next_rule_instance().value
        self.value = rule_manager.create_next_rule_instance().value + identifier_next
        self.is_byte = False

    def check(self):
        var = context_manager.get_variable(self.value)
        self.is_byte = var.original_var_type == 'char'
        if var is None:
            raise Exception('Variable "{}" has not been declared'.format(self.value))
        if not var.is_init:
            raise Exception('Variable "{}" has not been initialized before using'.format(self.value))

    def generate(self):
        if self.is_byte:
            generator_manager.print('(int)')
        generator_manager.print(self.value)

    def type(self):
        return context_manager.get_variable(self.value).var_type


class LetterDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        pass

    def generate(self):
        pass


class IdentifierNextDGN(DGN):
    def __init__(self, starts_with_digit, is_multiple):
        super().__init__()
        next_value = ''
        if is_multiple:
            next_value = rule_manager.create_next_rule_instance().value
        self.value = rule_manager.create_next_rule_instance().value + next_value

    def check(self):
        pass

    def generate(self):
        pass


class DigitDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(rule_manager.get_current_rule().rhs[0])

    def check(self):
        pass

    def generate(self):
        pass


class MainFunctionDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.function_body = None
        if has_body:
            self.function_body = rule_manager.create_next_rule_instance()

    def check(self):
        if self.function_body is not None:
            context_manager.push_scope()
            self.function_body.check()
            context_manager.pop_scope()

    def generate(self):
        generator_manager.println('int main() {')
        generator_manager.increase_tabs()
        if self.function_body is not None:
            self.function_body.generate()
        generator_manager.println()
        generator_manager.println('return 0;')
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class CodeFieldDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.instructions = [0]  # instruction list
        if is_multiple:
            self.instructions += rule_manager.create_next_rule_instance().instructions
        self.instructions[0] = rule_manager.create_next_rule_instance()

    def check(self):
        for instruction in self.instructions:
            instruction.check()

    def generate(self):
        for instruction in self.instructions:
            instruction.generate()
            generator_manager.println()


class InstructionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance()

    def check(self):
        self.value.check()

    def generate(self):
        self.value.generate()
        if self.what not in ['cycle', 'if_operator']:
            generator_manager.print(';')


class AssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.assignment_operator = rule_manager.create_next_rule_instance().value
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        var = context_manager.get_variable(self.identifier.value)
        if var is None:
            raise Exception('Cannot assign value to an undeclared variable "{}"'.format(self.identifier.value))
        self.expression.check()
        if self.identifier.type() != self.expression.type():
            raise Exception('Bad assignment to "{}": wrong rhs type'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print(' ')
        generator_manager.print(self.assignment_operator)
        generator_manager.print(' ')
        self.expression.generate()


class OperatorAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        pass


class ExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance()

    def check(self):
        self.value.check()

    def generate(self):
        self.value.generate()

    def type(self):
        return self.value.type()


class LogicalExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        if self.what in ['math_comparison', 'symb_comparison']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = rule_manager.create_next_rule_instance().value
            self.lhs = rule_manager.create_next_rule_instance()
        elif self.what == 'boolean_value':
            self.boolean_value = rule_manager.create_next_rule_instance()
        elif self.what == 'braced':
            self.expression = rule_manager.create_next_rule_instance()
        elif self.what in ['&&', '||']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = self.what
            self.lhs = rule_manager.create_next_rule_instance()
        else:
            self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        if self.what in ['math_comparison', 'symb_comparison', '&&', '||']:
            self.lhs.check()
            self.rhs.check()
            if self.lhs.type() != self.rhs.type():
                raise Exception('Wrong types!')
        elif self.what == 'braced':
            self.expression.check()

    def generate(self):
        if self.what in ['math_comparison', 'symb_comparison', '&&', '||']:
            self.lhs.generate()
            generator_manager.print(' ')
            generator_manager.print(self.operator)
            generator_manager.print(' ')
            self.rhs.generate()
        elif self.what == 'boolean_value':
            self.boolean_value.generate()
        elif self.what == 'braced':
            generator_manager.print('(')
            self.expression.generate()
            generator_manager.print(')')
        else:
            self.expression.generate()


    def type(self):
        return 'bool'


class MathExpressionDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what

        if self.what in ['+', '-', '*', '/', '%']:
            self.rhs = rule_manager.create_next_rule_instance()
            self.operator = rule_manager.create_next_rule_instance().value
            self.lhs = rule_manager.create_next_rule_instance()
        elif self.what in ['number', 'identifier', 'array1_element', 'array2_element']:
            self.value = rule_manager.create_next_rule_instance()
        else:
            self.value = rule_manager.create_next_rule_instance()

    def check(self):
        if self.what in ['+', '-', '*', '/', '%']:
            self.lhs.check()
            self.rhs.check()
            if self.lhs.type() != self.rhs.type():
                raise Exception('Wrong types!')
        elif self.what == 'identifier':
            var = context_manager.get_variable(self.value.value)
            self.value.check()
            if var is None:
                raise Exception('Variable "{}" has not been declared'.format(self.value.value))
            if var.var_type != 'number':
                raise Exception('Variable "{}" wrong type: {}'.format(self.value.value, var.var_type))
            if not var.is_init:
                raise Exception('Variable "{}" has not been initialized before using'.format(self.value.value))
            if self.value.type() != 'number':
                raise Exception('Variable "{}" type is not number'.format(self.value.value))
        elif self.what == 'array1_element' or self.what == 'array2_element':
            ...  # TODO make something
        elif self.what == 'function_call':
            self.value.check()
            if self.value.type() != 'number':
                raise Exception('Value type is not number'.format(self.value.value))

    def generate(self):
        if self.what in ['+', '-', '*', '/', '%']:
            self.lhs.generate()
            generator_manager.print(' ')
            generator_manager.print(self.operator)
            generator_manager.print(' ')
            self.rhs.generate()
        elif self.what == 'unary_minus':
            generator_manager.print('-')
            self.value.generate()
        elif self.what == 'braced':
            generator_manager.print('(')
            self.value.generate()
            generator_manager.print(')')
        elif self.what == 'number':
            generator_manager.print(self.value.value)
        elif self.what == 'identifier':
            self.value.generate()
        else:
            self.value.generate()

    def type(self):
        return 'number'


class AdditionSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)


class MultiplicationSignDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)


class NumberDGN(DGN):
    def __init__(self, what):
        super().__init__()
        self.what = what
        self.value = rule_manager.create_next_rule_instance().value

    def check(self):
        pass

    def generate(self):
        generator_manager.println(self.value)

    def type(self):
        return 'number'


class IntegerDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        next_value = ''
        if is_multiple:
            next_value = rule_manager.create_next_rule_instance().value
        self.value = rule_manager.create_next_rule_instance().value + next_value

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)

    def type(self):
        return 'number'


class RealNumberDGN(DGN):
    def __init__(self):
        super().__init__()
        rhs = rule_manager.create_next_rule_instance().value
        lhs = rule_manager.create_next_rule_instance().value
        self.value = lhs + '.' + rhs

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)

    def type(self):
        return 'number'


class CompareOperatorDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        pass


class SymbValueDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = '\'' + rule_manager.create_next_rule_instance().value + '\''

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)

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
        self.expression.check()
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
        self.value = str(''.join(rule_manager.get_current_rule().rhs))

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)

    def type(self):
        return 'bool'


class FunctionsDeclarationDGN(DGN):
    def __init__(self, multiple_declarations, has_params, has_body):
        super().__init__()
        self.functions = [dict()]
        if multiple_declarations:
            self.functions = self.functions + rule_manager.create_next_rule_instance().functions
        if has_body:
            self.functions[0]['body'] = rule_manager.create_next_rule_instance()
        if has_params:
            self.functions[0]['params'] = rule_manager.create_next_rule_instance()
        self.functions[0]['identifier'] = rule_manager.create_next_rule_instance().value
        self.functions[0]['return_type'] = rule_manager.create_next_rule_instance().value

    def check(self):
        for func in self.functions:
            if 'params' in func:
                params = list(map(lambda x: x[0], func['params'].value))
                context_manager.add_function(func['identifier'], params, func['return_type'])
            else:
                context_manager.add_function(func['identifier'], [], func['return_type'])

            context_manager.check_variable_does_not_exists(func['identifier'])
            context_manager.push_scope()
            if 'params' in func:
                func['params'].check()
            if 'body' in func:
                func['body'].check()
            context_manager.pop_scope()

    def generate(self):
        for func in self.functions:
            generator_manager.print(func['return_type'])
            generator_manager.print(' ')
            generator_manager.print(func['identifier'])
            generator_manager.print('(')
            if 'params' in func:
                func['params'].generate()
            generator_manager.println(') {')
            generator_manager.increase_tabs()
            if 'body' in func:
                func['body'].generate()
            generator_manager.decrease_tabs()
            generator_manager.println('}')
            generator_manager.println()


class FunctionReturnTypeDGN(DGN):
    def __init__(self, is_void):
        super().__init__()
        self.value = 'void'
        if not is_void:
            self.value = rule_manager.create_next_rule_instance().value

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)


class TypeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.value = str(''.join(rule_manager.get_current_rule().rhs))
        if self.value == 'boolean':
            self.value = 'bool'
        if self.value == 'byte':
            self.value = 'char'
        if self.value == 'long':
            self.value = 'long long'

    def check(self):
        pass

    def generate(self):
        generator_manager.print(self.value)

    def type(self):
        return self.value


class FunctionParamsDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()

        self.value = [(None, None)]

        if is_multiple:
            self.value = self.value + rule_manager.create_next_rule_instance().value
        self.value[0] = (rule_manager.create_next_rule_instance().value,
                         rule_manager.create_next_rule_instance().value)
        self.value[0] = self.value[0][1], self.value[0][0]

    def check(self):
        for var_type, var_name in self.value:
            context_manager.create_variable(var_name, var_type, True)

    def generate(self):
        generator_manager.print(', '.join(map(lambda x: x[0] + ' ' + x[1], self.value)))


class FunctionReturnDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        pass

    def generate(self):
        generator_manager.print('return ')
        self.expression.generate()


class VarDeclarationDGN(DGN):
    def __init__(self, is_init):
        super().__init__()
        self.is_init = is_init
        if is_init:
            self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance().value
        self.type = rule_manager.create_next_rule_instance().value

    def check(self):
        context_manager.check_variable_does_not_exists(self.identifier)
        context_manager.create_variable(self.identifier, self.type, self.is_init)
        if self.is_init:
            if context_manager.get_type(self.type) != self.expression.type():
                raise Exception('Bad initialization of variable "{}": wrong types'.format(self.identifier))

    def generate(self):
        generator_manager.print(self.type)
        generator_manager.print(' ')
        generator_manager.print(self.identifier)
        if self.is_init:
            generator_manager.print(' = ')
            self.expression.generate()


class FunctionCallDGN(DGN):
    def __init__(self, has_params, name=None):
        super().__init__()
        self.name = name
        self.params = None
        if has_params:
            self.params = rule_manager.create_next_rule_instance()
        if self.name is None:
            self.function_identifier = rule_manager.create_next_rule_instance().value

    def check(self):
        if self.params is not None:
            self.params.check()
            params = list(map(lambda x: x.type(), self.params.params))
            context_manager.check_function(self.name or self.function_identifier, params)
        else:
            context_manager.check_function(self.name or self.function_identifier, [])

    def generate(self):
        if self.name == 'System.out.print':
            generator_manager.print('std::cout << ')
            self.params.generate()
            return
        elif self.name == 'System.out.println':
            generator_manager.print('std::cout << ')
            self.params.generate()
            generator_manager.print(' << std::endl')
            return

        if self.name == 'Math.max':
            generator_manager.print('std::max(')
        elif self.name == 'Math.min':
            generator_manager.print('std::min(')
        else:
            generator_manager.print(self.function_identifier)
            generator_manager.print('(')
        if self.params is not None:
            self.params.generate()
        generator_manager.print(')')

    def type(self):
        if self.params is not None:
            self.params.check()
            params = list(map(lambda x: x.type(), self.params.params))
            return context_manager.get_return_type(self.name or self.function_identifier, params)
        else:
            return context_manager.get_return_type(self.name or self.function_identifier, [])


class FunctionCallParamsDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.params = [None]
        if is_multiple:
            self.params = self.params + rule_manager.create_next_rule_instance().params
        self.params[0] = rule_manager.create_next_rule_instance()

    def check(self):
        for param in self.params:
            param.check()

    def generate(self):
        self.params[0].generate()
        for i in range(1, len(self.params)):
            generator_manager.print(', ')
            self.params[i].generate()


class WhileDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.code_field = None
        if has_body:
            self.code_field = rule_manager.create_next_rule_instance()
        self.expression = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        context_manager.push_scope()
        if self.code_field is not None:
            self.code_field.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.print('while (')
        self.expression.generate()
        generator_manager.println(') {')
        generator_manager.increase_tabs()
        if self.code_field is not None:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class DoWhileDGN(DGN):
    def __init__(self, has_body):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.code_field = None
        if has_body:
            self.code_field = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        context_manager.push_scope()
        if self.code_field is not None:
            self.code_field.check()
        context_manager.pop_scope()

    def generate(self):
        generator_manager.println('do {')
        generator_manager.increase_tabs()
        if self.code_field is not None:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.print('} while (')
        self.expression.generate()
        generator_manager.println(');')


class ForDGN(DGN):
    def __init__(self, is_initialization, has_body):
        super().__init__()
        self.code_field = None
        if has_body:
            self.code_field = rule_manager.create_next_rule_instance()
        self.move_assignment = rule_manager.create_next_rule_instance()
        self.logical_expression = rule_manager.create_next_rule_instance()
        self.assignment = rule_manager.create_next_rule_instance()

    def check(self):
        context_manager.push_scope()
        self.assignment.check()
        self.logical_expression.check()
        self.move_assignment.check()
        if self.code_field is not None:
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
        if self.code_field is not None:
            self.code_field.generate()
        generator_manager.decrease_tabs()
        generator_manager.println('}')


class StringLiteralDGN(DGN):
    def __init__(self, is_not_empty):
        super().__init__()
        self.value = ''
        if is_not_empty:
            self.value = rule_manager.create_next_rule_instance().value

    def check(self):
        pass

    def generate(self):
        generator_manager.print('"')
        generator_manager.print(self.value)
        generator_manager.print('"')

    def type(self):
        return 'String'


class StringLettersDGN(DGN):
    def __init__(self, is_multiple):
        super().__init__()
        self.value = ''
        if is_multiple:
            self.value = rule_manager.create_next_rule_instance().value
        self.value = rule_manager.create_next_rule_instance().value + self.value

    def check(self):
        pass

    def generate(self):
        pass


class Array1InitializationDGN(DGN):
    def __init__(self):
        super().__init__()
        self.size = rule_manager.create_next_rule_instance()
        self.rhs_type = rule_manager.create_next_rule_instance().value
        self.identifier = rule_manager.create_next_rule_instance()
        self.lhs_type = rule_manager.create_next_rule_instance().value

    def check(self):
        if self.lhs_type != self.rhs_type:
            raise Exception(f'Cannot cast an array of type {self.rhs_type} to an array of type {self.lhs_type}')
        self.size.check()
        context_manager.create_array(self.identifier.value, self.lhs_type, dims=1)

    def generate(self):
        generator_manager.print('std::vector<')
        generator_manager.print(self.lhs_type)
        generator_manager.print('> ')
        generator_manager.print(self.identifier.value)
        generator_manager.print('(')
        self.size.generate()
        generator_manager.print(')')


class Array2InitializationDGN(DGN):
    def __init__(self):
        super().__init__()
        self.size2 = rule_manager.create_next_rule_instance()
        self.size1 = rule_manager.create_next_rule_instance()
        self.rhs_type = rule_manager.create_next_rule_instance().value
        self.identifier = rule_manager.create_next_rule_instance()
        self.lhs_type = rule_manager.create_next_rule_instance().value

    def check(self):
        if self.lhs_type != self.rhs_type:
            raise Exception(f'Cannot cast an array of type {self.rhs_type} to an array of type {self.lhs_type}')
        self.size1.check()
        self.size2.check()
        context_manager.create_array(self.identifier.value, self.lhs_type, dims=2)

    def generate(self):
        generator_manager.print('std::vector<std::vector<')
        generator_manager.print(self.lhs_type)
        generator_manager.print('>> ')
        generator_manager.print(self.identifier.value)
        generator_manager.print('(')
        self.size1.generate()
        generator_manager.print(', std::vector<')
        generator_manager.print(self.lhs_type)
        generator_manager.print('>(')
        self.size2.generate()
        generator_manager.print('))')


class Array1ElementAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.operator = rule_manager.create_next_rule_instance().value
        self.array1element = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        self.array1element.check()
        if self.array1element.identifier.type() != self.expression.type():
            raise Exception('Bad assignment to "{}[]": wrong rhs type'.format(self.array1element.identifier.value))

    def generate(self):
        self.array1element.generate()
        generator_manager.print(' ')
        generator_manager.print(self.operator)
        generator_manager.print(' ')
        self.expression.generate()


class Array2ElementAssignmentDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.operator = rule_manager.create_next_rule_instance().value
        self.array2element = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        self.array2element.check()
        if self.array2element.type() != self.expression.type():
            raise Exception('Bad assignment to "{}[]": wrong rhs type'.format(self.array2element.identifier.value))

    def generate(self):
        self.array2element.generate()
        generator_manager.print(' ')
        generator_manager.print(self.operator)
        generator_manager.print(' ')
        self.expression.generate()


class Array1ElementDGN(DGN):
    def __init__(self):
        super().__init__()
        self.index = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.index.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'array1':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('[')
        self.index.generate()
        generator_manager.print(']')

    def type(self):
        return self.identifier.type()


class Array2ElementDGN(DGN):
    def __init__(self):
        super().__init__()
        self.index2 = rule_manager.create_next_rule_instance()
        self.index1 = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.index1.check()
        self.index2.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'array2':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('[')
        self.index1.generate()
        generator_manager.print(']')
        generator_manager.print('[')
        self.index2.generate()
        generator_manager.print(']')

    def type(self):
        return self.identifier.type()


class ArraylistInitializationDGN(DGN):
    def __init__(self, cpp_type):
        super().__init__()
        self.cpp_type = cpp_type
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        context_manager.create_arraylist(self.identifier.value, self.cpp_type)

    def generate(self):
        generator_manager.print('std::vector<')
        generator_manager.print(self.cpp_type)
        generator_manager.print('> ')
        generator_manager.print(self.identifier.value)


class ArraylistAddDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('.push_back(')
        self.expression.generate()
        generator_manager.print(')')


class ArraylistClearDGN(DGN):
    def __init__(self):
        super().__init__()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('.clear()')


class ArraylistRemoveDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('.erase(')
        generator_manager.print(self.identifier.value)
        generator_manager.print('.begin() + (')
        self.expression.generate()
        generator_manager.print('))')


class ArraylistGetDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('[')
        self.expression.generate()
        generator_manager.print(']')

    def type(self):
        return self.identifier.type()


class ArraylistSizeDGN(DGN):
    def __init__(self):
        super().__init__()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('.size()')

    def type(self):
        return 'number'


class ArraylistContainsDGN(DGN):
    def __init__(self):
        super().__init__()
        self.expression = rule_manager.create_next_rule_instance()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        self.expression.check()
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print('(')
        generator_manager.print(self.identifier.value)
        generator_manager.print('.end() != std::find(')
        generator_manager.print(self.identifier.value)
        generator_manager.print('.begin(), ')
        generator_manager.print(self.identifier.value)
        generator_manager.print('.end(), ')
        self.expression.generate()
        generator_manager.print('))')

    def type(self):
        return 'bool'


class ArraylistIsEmptyDGN(DGN):
    def __init__(self):
        super().__init__()
        self.identifier = rule_manager.create_next_rule_instance()

    def check(self):
        var = context_manager.get_variable(self.identifier.value)
        if var is None or var.what != 'arraylist':
            raise Exception('Variable "{}" has not been declared'.format(self.identifier.value))

    def generate(self):
        generator_manager.print(self.identifier.value)
        generator_manager.print('.empty()')

    def type(self):
        return 'bool'
