
class RuleManager:
    def __init__(self, rules):
        self.rules = rules
        self.rp = len(rules) - 1

    def get_current_rule(self):
        return self.rules[self.rp]

    def get_next_rule(self):
        self.rp -= 1
        return self.rules[self.rp]

    def create_current_rule_instance(self):
        return self.rules[self.rp].cls(**self.rules[self.rp].kwargs)

    def create_next_rule_instance(self):
        self.rp -= 1
        return self.rules[self.rp].cls(**self.rules[self.rp].kwargs)


rule_manager = RuleManager([])


def build_tree(rules):
    global rule_manager
    rule_manager = RuleManager(rules)
    root = rule_manager.create_current_rule_instance()

    return root
