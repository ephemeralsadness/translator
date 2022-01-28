from translator.constants import KEYWORDS


class ContextManager:
    def __init__(self):
        self.scopes = []
        self.functions = dict()
        self.keywords = KEYWORDS

    def push_scope(self):
        self.scopes.append(dict())

    def pop_scope(self):
        self.scopes.pop()

    def type_of_variable(self, var_name):
        for scope in self.scopes:
            if var_name in scope:
                return scope[var_name]
        return None, None

    def set_type_of_variable(self, var_name, var_type, is_inited):
        self.scopes[len(self.scopes) - 1][var_name] = (var_type, is_inited)

    def make_function(self, name, args, return_type):
        self.functions[name, args] = return_type

    def get_function_return_type(self, name, args):
        if (name, args) in self.functions:
            return self.functions[name, args]


context_manager = ContextManager()
