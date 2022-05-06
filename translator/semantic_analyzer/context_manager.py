import collections

from translator.constants import KEYWORDS, VARIABLE_TYPES
from collections import namedtuple

Variable = namedtuple('Variable', ['var_type', 'is_init', 'original_var_type', 'what'])


class ContextManager:
    def __init__(self):
        self.scopes = []
        self.functions = dict()
        self.keywords = KEYWORDS
        for var_type in VARIABLE_TYPES:
            self.add_function('System.out.println', [var_type], 'void')
            self.add_function('System.out.print', [var_type], 'void')
            self.add_function('Math.min', [var_type, var_type], 'number')
            self.add_function('Math.max', [var_type, var_type], 'number')

    def push_scope(self):
        self.scopes.append(dict())

    def pop_scope(self):
        self.scopes.pop()

    def check_variable_does_not_exists(self, name):
        if name in KEYWORDS:
            raise Exception(f'Unexpected reserved name for a variable "{name}"')
        if name in self.functions:
            raise Exception(f'Mismatch function/variable "{name}"')
        for scope in self.scopes:
            if name in scope:
                raise Exception(f'Variable with name "{name}" has been already declared')

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
        if var_type in ['int', 'float', 'double', 'char', 'short', 'long', 'byte']:
            return 'number'
        return var_type

    def add_function(self, name, args, return_type):
        real_args = list(map(lambda x: self.get_type(x), args))
        real_name = name + str(real_args)
        self.functions[real_name] = self.get_type(return_type)

    def check_function(self, name, args):
        real_args = list(map(lambda x: self.get_type(x), args))
        real_name = name + str(real_args)
        if real_name not in self.functions:
            raise Exception(f'Cannot resolve function name "{name}"')

    def get_return_type(self, name, args):
        real_args = list(map(lambda x: self.get_type(x), args))
        self.check_function(name, args)
        return self.functions[name + str(real_args)]


context_manager = ContextManager()
