from Symbol import *
from typing import Dict

statements = {
    'main': Sym(PRINCIPAL, 'main'),
    'return': Sym(REGRESA, 'return'),
    'if': Sym(SI, 'if'),
    'else': Sym(ELSE, 'else'),
    'while': Sym(MIENTRAS, 'while')
}
data_types = {
    'int': Sym(ENTERO, 'int'),
    'float': Sym(LOGICO, 'float'),
    'void': Sym(VOID, 'void')
}
booleans = {
    'true': Sym(VERDADERO, 'true'),
    'false': Sym(FALSO, 'false')
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
    '(': Sym(LEFT_PAR, '('),
    ')': Sym(RIGHT_PAR, ')'),
    '{': Sym(LEFT_CURL, '{'),
    '}': Sym(RIGHT_CURL, '}'),
    '[': Sym(LEFT_BRACKET, '['),
    ']': Sym(RIGHT_BRACKET, ']')
}

KeywordType = Dict[str, Sym]
not_ids = statements.copy()
not_ids.update(data_types)
not_ids.update(booleans)
__all__ = not_ids.copy()
__all__.update(arithmetic_ops)
__all__.update(relational_ops)
__all__.update(boolean_ops)
__all__.update(assignment)
__all__.update(punctuation)
