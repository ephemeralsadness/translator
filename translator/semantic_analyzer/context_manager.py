import collections

from translator.constants import KEYWORDS
from collections import namedtuple

Variable = namedtuple('Variable', ['var_type', 'is_init', 'original_var_type', 'what'])


class ContextManager:
    def __init__(self):
        self.scopes = []
        self.functions = dict()
        self.keywords = KEYWORDS
        self.add_function('System.out.println', 1, 'void')
        self.add_function('System.out.print', 1, 'void')
        self.add_function('Math.min', 2, 'number')
        self.add_function('Math.max', 2, 'number')

    def push_scope(self):
        self.scopes.append(dict())

    def pop_scope(self):
        self.scopes.pop()

    def check_variable_does_not_exists(self, name):
        if name in KEYWORDS:
            raise Exception('Unexpected reserved name for a variable "{}"'.format(name))
        if name in self.functions:
            raise Exception('Mismatch function/variable "{}"'.format(name))
        for scope in self.scopes:
            if name in scope:
                raise Exception('Variable with name "{}" has been already declared'.format(name))

    def create_variable(self, name, var_type, is_init):
        self.check_variable_does_not_exists(name)
        self.scopes[len(self.scopes) - 1][name] = Variable(self.get_type(var_type), is_init, var_type, 'var')

    def create_array(self, name, var_type, dims):
        self.check_variable_does_not_exists(name)
        self.scopes[len(self.scopes) - 1][name] = Variable(self.get_type(var_type), True, var_type, f'array{dims}')

    def create_arraylist(self, name, var_type):
        self.check_variable_does_not_exists(name)
        self.scopes[len(self.scopes) - 1][name] = Variable(self.get_type(var_type), True, var_type, 'arraylist')

    def get_variable(self, name):
        for scope in self.scopes:
            if name in scope:
                return scope[name]
        return None

    def get_type(self, var_type):
        if var_type in ['int', 'float', 'double', 'char', 'short', 'long']:
            return 'number'
        return var_type

    def add_function(self, name, args_size, return_type):
        real_name = name + ' ' + str(args_size)
        self.functions[real_name] = self.get_type(return_type)

    def check_function(self, name, args_size):
        real_name = name + ' ' + str(args_size)
        if real_name not in self.functions:
            raise Exception('Cannot resolve function name "{}"'.format(name))

    def get_return_type(self, name, args_size):
        self.check_function(name, args_size)
        return self.functions[name + ' ' + str(args_size)]


context_manager = ContextManager()
