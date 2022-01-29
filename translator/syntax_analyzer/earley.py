#!/usr/bin/env python3
import string
import sys
from enum import Enum
from translator.syntax_analyzer.rules import Rule, java_rules

class Grammar(object):
    def __init__(self, rules, start_rule):
        self.rules = {}
        self.start_rule = start_rule

        for rule in rules:
            if rule.lhs not in self.rules:
                self.rules[rule.lhs] = [rule]
            else:
                self.rules[rule.lhs].append(rule)

    def __repr__(self):
        return '\n'.join(map(
            lambda rules: '\n'.join(map(str, rules)),
            self.rules.values()
        ))


class EarleyItem(object):
    def __init__(self, rule, start, dot, prev=[]):
        self.rule = rule
        self.start = start
        self.dot = dot
        self.prev = prev[:]

    def __eq__(self, other):
        return isinstance(other, EarleyItem) and \
               self.rule == other.rule and \
               self.start == other.start and \
               self.dot == other.dot

    def __repr__(self):
        rhs = self.rule.rhs[:]
        rhs.insert(self.dot, '•')

        return f'{self.rule.lhs} -> {" ".join(map(str, rhs))} ({self.start})'


class ItemSet(list):
    def append(self, val):
        if not list.__contains__(self, val):
            list.append(self, val)

    def extend(self, values):
        for val in values:
            self.append(val)


class EarleyState(Enum):
    Complete = 0
    Terminal = 1
    NonTerminal = 2


def next_symb(earley_item, terminals):
    symb = None
    state = EarleyState.Complete

    if earley_item.dot < len(earley_item.rule.rhs):
        symb = earley_item.rule.rhs[earley_item.dot]
        state = EarleyState.Terminal if symb in terminals else EarleyState.NonTerminal

    return state, symb


def predict(grammar, item_set, symb, i):
    item_set.extend([EarleyItem(rule, i, 0) for rule in grammar.rules[symb]])


def scan(earley_item_set, item, symb, word, i):
    if symb == word:
        earley_item_set[i + 1].append(EarleyItem(
            item.rule, item.start, item.dot + 1, item.prev[:]
        ))


def complete(earley_item_set, item_set, item, terminals):
    item_set.extend(map(
        lambda it: EarleyItem(it.rule, it.start, it.dot + 1, it.prev + [item]),
        filter(
            lambda old_item: next_symb(old_item, terminals)[1] == item.rule.lhs,
            earley_item_set[item.start]
        )
    ))


def earley(grammar, terminals, sentence):
    earley_item_set = list(map(ItemSet, [
        [EarleyItem(rule, 0, 0) for rule in grammar.rules[grammar.start_rule]],
        *[[] for _ in range(len(sentence))]
    ]))

    for i, (word, item_set) in enumerate(zip(sentence, earley_item_set)):
        for item in item_set:
            state, symb = next_symb(item, terminals)

            if state is EarleyState.Complete:
                complete(earley_item_set, item_set, item, terminals)
            elif state is EarleyState.NonTerminal:
                predict(grammar, item_set, symb, i)
            elif state is EarleyState.Terminal:
                scan(earley_item_set, item, symb, word, i)

    for item in earley_item_set[-1]:
        state, symb = next_symb(item, terminals)

        if state is EarleyState.Complete:
            complete(earley_item_set, earley_item_set[-1], item, terminals)

    return earley_item_set


def to_lr(item):
    return sum(map(to_lr, item.prev), []) + [item.rule]


def make_right_parsing(whitespace_tokens):
    start_rule = '~program~'
    terminals = set(string.digits + string.ascii_letters + string.whitespace + '_(){}[]+-*/%><=!&|;,"\'.#@№$^:?')

    grammar = Grammar(java_rules, start_rule)

    earley_set = earley(grammar, terminals, whitespace_tokens)

    if len(earley_set) != len(whitespace_tokens) + 1:
        raise Exception('Incorrect sentence')

    for item in earley_set[-1]:
        if item.dot == len(item.rule.rhs) and \
                item.start == 0 and \
                item.rule.lhs == start_rule:
            last = item
            break
    else:
        index = 0
        for i, list in enumerate(earley_set):
            if len(list) == 0:
                index = i
                break
        first_line = whitespace_tokens[index-10:index+10]+'\n'
        second_line = ' '*7 + '^^^^' + ' '*9
        raise Exception('Incorrect sentence, symb # {}\n'.format(index)+first_line+second_line)

    return to_lr(last)
