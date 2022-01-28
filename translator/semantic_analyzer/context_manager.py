from translator.constants import KEYWORDS

class ContextManager:
    def __init__(self):
        self.scopes = []
        self.keywords = KEYWORDS
    def push_scope(self):
        self.scopes.append(dict())

    def pop_scope(self):
        self.scopes.append(dict())

    def type_of_variable(self, var_name):
        for scope in self.scopes:
            if var_name in scope:
                return scope[var_name]
        return None

    def set_type_of_variable(self, var_name, var_type, is_inited):
        self.scopes[len(self.scopes) - 1][var_name] = (var_type, is_inited)

context_manager = ContextManager()
