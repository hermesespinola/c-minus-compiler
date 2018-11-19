from Symbol import *
from typing import Dict

statements = {
    'a': Sym(A, 'a'),
    'class': Sym(CLASS, 'class'),
    'is': Sym(IS, 'is'),
    'he': Sym(PRONOUN, 'he'),
    'she': Sym(PRONOUN, 'she'),
    'it': Sym(PRONOUN, 'it'),
    'has': Sym(HAS, 'has'),
    'equal': Sym(EQUALS, 'equal'),
    'equals': Sym(EQUALS, 'equals'),
    'to': Sym(TO, 'to'),
    'can': Sym(CAN, 'can'),
    'needs': Sym(NEEDS, 'needs'),
    'his': Sym(POSESIVE, 'his'),
    'her': Sym(POSESIVE, 'her'),
    'its': Sym(POSESIVE, 'its'),
    'and': Sym(BOOLEAN_OP, 'and'),
    'or': Sym(BOOLEAN_OP, 'or'),
    'not': Sym(BOOLEAN_OP, 'not'),
    'by': Sym(BY, 'by'),
    'as': Sym(AS, 'as'),
    'if': Sym(IF, 'if'),
    'with': Sym(WITH, 'with'),
    'while': Sym(WHILE, 'while'),
    'greater': Sym(GT, 'greater'),
    'less': Sym(LT, 'less'),
    'than': Sym(THAN, 'than'),
    'lets': Sym(LETS, 'lets'),
    'increments': Sym(INCREMENTS, 'increments'),
    'decreases': Sym(DECREASES, 'decreases'),
    '\n': Sym(LINE_BREAK, '\n'),
    'says': Sym(SAYS, 'says'),
}
arithmetic_ops = {
    '+': Sym(PLUS, '+'),
    '-': Sym(MINUS, '-'),
    '*': Sym(TIMES, '*'),
    '/': Sym(DIV, '/')
}
relational_ops = {
    '>': Sym(GT, '>'),
    '<': Sym(LT, '<'),
    '==': Sym(EQ, '=='),
    '!=': Sym(NOT_EQ, '!='),
    '>=': Sym(GEQ, '>='),
    '<=': Sym(LEQ, '<=')
}
boolean_ops = {
    '&': Sym(AND, '&'),
    '|': Sym(OR, '|'),
    '!': Sym(NOT, '!')
}
assignment = {
    '=': Sym(ASS, '=')
}
punctuation = {
    ',': Sym(COMMA, ','),
    ';': Sym(SEMMI, ';'),
    '.': Sym(DOT, '.'),
    '(': Sym(LEFT_PAR, '('),
    ')': Sym(RIGHT_PAR, ')'),
    '{': Sym(LEFT_CURL, '{'),
    '}': Sym(RIGHT_CURL, '}'),
    '[': Sym(LEFT_BRACKET, '['),
    ']': Sym(RIGHT_BRACKET, ']')
}

KeywordType = Dict[str, Sym]
not_ids = statements.copy()
__all__ = not_ids.copy()
__all__.update(arithmetic_ops)
__all__.update(relational_ops)
__all__.update(boolean_ops)
__all__.update(assignment)
__all__.update(punctuation)
