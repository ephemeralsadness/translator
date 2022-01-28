

class Expression:
    def __init__(self):
        ...

    def calculate(self):
        ...

    def check(self):
        ...


class ArithmeticExpression(Expression):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        self.rhs = rule_manager.create_next_rule_instance()
        self.lhs = rule_manager.create_next_rule_instance()

    def calculate(self):
        if self.operator == '+':
            return self.lhs.calculate() + self.rhs.calculate()
        if self.operator == '-':
            return self.lhs.calculate() - self.rhs.calculate()
        if self.operator == '*':
            return self.lhs.calculate() * self.rhs.calculate()
        if self.operator == '/':
            return self.lhs.calculate() / self.rhs.calculate()

    def check(self):
        self.lhs.check()
        self.rhs.check()
        if self.operator == '/' and self.rhs.calculate() == 0:
            raise Exception('Division by zero!')


class BracedExpression(Expression):
    def __init__(self):
        super().__init__()
        self.expr = rule_manager.create_next_rule_instance()

    def calculate(self):
        return self.expr.calculate()

    def check(self):
        self.expr.check()


class Digit(Expression):
    def __init__(self):
        super().__init__()
        self.expr = rule_manager.create_next_rule_instance()

    def calculate(self):
        return self.expr.calculate()

    def check(self):
        self.expr.check()


class Terminal(Expression):
    def __init__(self):
        super().__init__()
        self.digit = int(rule_manager.get_current_rule().rhs[0])

    def calculate(self):
        return self.digit

    def check(self):
        ...