from translator.syntax_analyzer.earley import Rule


def ct(a):
    b = []
    for x in a:
        b.append(x)
        b.append('`')
    b.pop(len(b) - 1)
    return b


rules = [
    Rule('<program>', ct(['class', '<id>', '{', '<main_function>', '}'])),
    Rule('<program>', ct(['class', '<id>', '{', '<function_declarations>', '<main_function>', '}'])),
    Rule('<main_function>', ct(['public', 'static', 'void', 'main', '(', 'String', '[', ']', 'args', ')',
                                '{', '<code>', '}'])),
    Rule('<variable_declaration>', ct(['<type>', '<id>'])),
    Rule('<variable_declaration>', ct(['<type>', '<id>', '=', '<value>'])),


    Rule('expr', ['expr', '-', 'expr']),
    Rule('expr', ['expr', '*', 'expr']),
    Rule('expr', ['expr', '/', 'expr']),
    Rule('expr', ['(', 'expr', ')']),
    Rule('expr', ['term']),
    *[Rule('term', [str(i)]) for i in range(10)]
]