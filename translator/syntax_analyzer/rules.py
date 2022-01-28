
class Rule(object):
    def __init__(self, lhs, rhs, cls, **kwargs):
        self.lhs = lhs
        self.rhs = rhs
        self.cls = cls
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.lhs} -> {" ".join(self.rhs)}'


def ct(a):
    b = []
    for x in a:
        b.append(x)
        b.append('`')
    b.pop(len(b) - 1)
    return b


java_rules = [
    Rule('/program\\', ct(['class', '/id\\', '{', '/main_function\\', '}'])),
    Rule('/program\\', ct(['class', '/id\\', '{', '/function_declarations\\', '/main_function\\', '}'])),

    Rule('/main_function\\',
         ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{', '/code\\', '}'])),

    Rule('/variable_declaration\\', ct(['/type\\', '/id\\'])),
    Rule('/variable_declaration\\', ct(['/type\\', '/id\\', '=', '/value\\'])),

    Rule('/funcrion_declaration\\', ct(['/function_type\\', '/id\\', '(', '/params\\', ')', ';'])),
    Rule('/funcrion_declaration\\', ct(['/function_type\\', '/id\\', '(', '/params\\', ')', '{' '/code\\', '}'])),

    Rule('/params\\', ct(['/type\\', '/id\\', '/params\\'])),
    Rule('/params\\', ct([''])),

    Rule('/significant_type\\', ct(['bool'])),
    Rule('/significant_type\\', ct(['char'])),
    Rule('/significant_type\\', ct(['int'])),
    Rule('/significant_type\\', ct(['float'])),
    Rule('/significant_type\\', ct(['double'])),
    Rule('/significant_type\\', ct(['string'])),

    Rule('/type\\', ct(['/modifier\\', '/significant_type\\'])),
    Rule('/type\\', ct(['/significant_type\\'])),

    Rule('/function_type\\', ['/type\\']),
    Rule('/function_type\\', ct(['void'])),
    Rule('/function_type\\', ct(['void'])),

    *[Rule('/letter\\', [letter]) for letter in ascii_letters],
    *[Rule('/digit\\', [str(i)]) for i in range(10)],

    Rule('/int_number\\', ['/digit\\', '/int_number\\']),
    Rule('/int_number\\', ['/digit\\']),

    Rule('/float_number\\', ['/int_number\\', '.', '/int_number\\']),

    Rule('/number\\', ['/int_number']),
    Rule('/number\\', ['/float_number']),

    *[Rule('/others\\', [letter]) for letter in others],

    Rule('/letter_id\\', ['/letter\\']),
    Rule('/letter_id\\', ['_']),

    Rule('/id\\', ct(['/letter_id'])),
    Rule('/id\\', ct(['/letter_id', '/id\\'])),
    Rule('/id\\', ct(['/digit'])),
    Rule('/id\\', ct(['/digit', '/id\\'])),

    Rule('/code\\', ct(['/code_block\\', '/return\\'])),
    Rule('/code\\', ['/code_block\\']),

    Rule('/return\\', ct(['return', '/expression\\', ';'])),
    Rule('/return\\', ct(['return', '/variable_id\\', ';'])),
    Rule('/return\\', ct(['return', '/const_id\\', ';'])),

    Rule('/code_block\\', ct(['/instruction\\', ';' '/code_block\\'])),
    Rule('/code_block\\', ct(['/instruction\\', ';'])),

    Rule('/loop\\', ct(['while', '(', '/expression\\', ')' '{', '/code_block\\', '}'])),
    Rule('/loop\\', ct(['do', '{', '/code_block\\', '}', '(', '/expression\\', ')'])),
    Rule('/loop\\',
         ct(['for', '(', '/instruction\\', ';', '/logic_expression\\', '/assignment\\', ')' '{', '/code_block\\',
             '}'])),
    Rule('/loop\\',
         ct(['for', '(', '/letter_id\\', ';', '/logic_expression\\', '/assignment\\', ')' '{', '/code_block\\', '}'])),

    Rule('/symbol\\', ['\'letter\'']),
    Rule('/symbol\\', ['\'digit\'']),
    Rule('/symbol\\', ['\'others\'']),

    Rule('/branching\\', ct(['if', '(', '/expression\\', ')', '{', '/code_block\\', '}'])),
    Rule('/branching\\',
         ct(['if', '(', '/expression\\', ')', '{', '/code_block\\', '}', 'else', '{', '/code_block\\', '}'])),
    Rule('/branching\\', ct(['if', '(', '/expression\\', ')', '{', '/code_block\\', '}', 'else', '/branching\\'])),

    Rule('/comparison\\', ['==']),
    Rule('/comparison\\', ['!=']),
    Rule('/comparison\\', ['>']),
    Rule('/comparison\\', ['<']),
    Rule('/comparison\\', ['>=']),
    Rule('/comparison\\', ['<=']),

    Rule('/math_add\\', ['+']),
    Rule('/math_add\\', ['-']),

    Rule('/math_mul\\', ['*']),
    Rule('/math_mul\\', ['/']),
    Rule('/math_mul\\', ['%']),

    Rule('/math_expression\\', ['/int_number\\']),
    Rule('/math_expression\\', ['/float_number\\']),
    Rule('/math_expression\\', ct(['/math_expression\\', '/math_add\\', '/math_expression\\'])),
    Rule('/math_expression\\', ct(['/math_expression\\', '/math_mul\\', '/math_expression\\'])),
    Rule('/math_expression\\', ['/id\\']),
    Rule('/math_expression\\', ct(['(', '/math_expression\\', ')'])),

    Rule('/logical_value\\', ['true']),
    Rule('/logical_value\\', ['false']),

    Rule('/logical_add\\', ['||']),
    Rule('/logical_add\\', ['/comparison\\']),

    Rule('/logical_mul\\', ['&&']),

    Rule('/logical_expression\\', ['/logical_value\\']),
    Rule('/logical_expression\\', ct(['/math_expression\\', '/comparison', 'math_expression'])),
    Rule('/logical_expression\\', ct(['/symbol\\', '/comparison', 'symbol'])),

    Rule('/instruction\\', ['/assignment\\']),
    Rule('/instruction\\', ['/variable_declaration\\']),
    Rule('/instruction\\', ['/function_call\\']),
    Rule('/instruction\\', ['/expression\\']),
    Rule('/instruction\\', ['/loop\\']),
    Rule('/instruction\\', ['/branching\\']),

    Rule('/function_call\\', ct(['/id\\', '(', ')'])),
    Rule('/function_call\\', ct(['/id\\', '(', '/call_params\\', ')'])),
    Rule('/function_call\\', ct(['System.out.println', '(', '/expression\\', ')'])),
    Rule('/function_call\\', ct(['Math.min', '(', '/expression\\', '/expression\\', ')'])),

    Rule('/call_params\\', ['/expression\\']),
    Rule('/call_params\\', ['/expression\\', ',', '/expression\\']),

    Rule('/assignment_operator\\', ['=']),
    Rule('/assignment_operator\\', ['+=']),
    Rule('/assignment_operator\\', ['-=']),
    Rule('/assignment_operator\\', ['\=']),
    Rule('/assignment_operator\\', ['%=']),
    Rule('/assignment_operator\\', ['*=']),

    Rule('/assignment', ct(['/id\\', '/assignment_operator\\', '/expression\\'])),
    Rule('/assignment', ct(['/id\\', '/assignment_operator\\', '/id\\'])),

    Rule('/expression\\', ['/logical_expression\\']),
    Rule('/expression\\', ['/math_expression\\']),
    Rule('/expression\\', ['/symbol\\']),
    Rule('/expression\\', ['/id\\']),
    Rule('/expression\\', ['/function_call\\']),
]