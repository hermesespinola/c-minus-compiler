from FuncSymTable import FunctionSymbolTable
from token import Token
from Symbol import *
from typing import Tuple, Dict, List
from syntax_tree import *

def throwSyntaxError(msg):
    raise Exception(msg)

def check_token_type(token: Token, keyword_type):
    if token.value() not in keyword_type:
        value = token.value()
        throwSyntaxError('Esperaba un tipo de dato pero se encontró {} en linea {}, columna {}'.format(value, token.line, token.col))
    return token.symbol.kind

def check_token(token: Token, kind: int):
    if not token.isK(kind):
        throwSyntaxError('Esperaba {} pero se encontró {} en linea {}, columna {}'.format(SymEnum(kind).name, token.value(), token.line, token.col))

def class_declaration(tokens: List[Token]):
    check_token(tokens[0], A)
    check_token(tokens[1], ID)
    check_token(tokens[2], IS)
    check_token(tokens[3], A)
    check_token(tokens[4], CLASS)
    return tokens[5:]

def factor(tokens):
    if tokens[0].isK(ID) or tokens[0].isK(NUM):
        return tokens[1:]
    else:
        check_token(tokens[0], LEFT_PAR)
        tokens = simple_expression(tokens[1:])
        check_token(tokens[0], RIGHT_PAR)
        return tokens[1:]

def term(tokens):
    tokens = factor(tokens)
    if tokens[0].symbol.kind in [TIMES, DIV]:
        tokens = term(tokens[1:])
    return tokens

def additive_expression(tokens):
    tokens = term(tokens)
    if tokens[0].inK([PLUS, MINUS]):
        tokens = additive_expression(tokens[1:])
    return tokens

def simple_expression(tokens):
    # El de a de veras
    tokens = additive_expression(tokens)
    if tokens[0].inK(COMPARISON_OPERATORS):
        tokens = additive_expression(tokens[1:])
    return tokens

def math_or_string_expression(tokens):
    if tokens[0].isK(STRING):
        return tokens[1:]
    else:
        return simple_expression(tokens)

def attribute(tokens: List[Token]):
    # init and assign
    check_token(tokens[0], ID)
    if tokens[1].isK(EQUALS):
        check_token(tokens[2], TO)
        tokens = math_or_string_expression(tokens[3:])
        return tokens[0:]
    else:
        return tokens[1:]

def attribute_declaration(tokens: List[Token]):
    check_token(tokens[0], PRONOUN)
    if not tokens[1].isK(HAS):
            return tokens
    tokens = tokens[2:]
    while tokens[0].isK(ID):
        tokens = attribute(tokens)
        # end attribute declarations
        if tokens[0].isK(DOT):
            return tokens[1:]
        check_token(tokens[0], COMMA)
        if tokens[1].value() == 'and':
            tokens = tokens[2:]
        else:
            tokens = tokens[1:]
    return tokens

def method_declaration(tokens: List[Token]):
    check_token(tokens[0], PRONOUN)
    if not tokens[1].isK(CAN):
            return tokens
    tokens = tokens[2:]
    while tokens[0].isK(ID):
        # end method declarations
        if tokens[1].isK(DOT):
            return tokens[2:]
        check_token(tokens[1], COMMA)
        if tokens[2].value() == 'and':
            tokens = tokens[3:]
        else:
            tokens = tokens[2:]
    return tokens

def print_expression(tokens):
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], SAYS)
    return math_or_string_expression(tokens[2:])

def decrement_expression(tokens):
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], DECREASES)
    if tokens[2].isK(POSESIVE):
        tokens = tokens[3:]
    else:
        tokens = tokens[2:]
    check_token(tokens[0], ID)
    check_token(tokens[1], BY)
    check_token(tokens[2], NUM)
    return tokens[3:]

def increment_expression(tokens):
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], INCREMENTS)
    if tokens[2].isK(POSESIVE):
        tokens = tokens[3:]
    else:
        tokens = tokens[2:]
    check_token(tokens[0], ID)
    check_token(tokens[1], BY)
    check_token(tokens[2], NUM)
    return tokens[3:]

def function_arguments(tokens):
    check_token(tokens[0], ID)
    check_token(tokens[1], AS)
    tokens = math_or_string_expression(tokens[2:])

    while tokens[0].isK(COMMA):
        if tokens[1].value() == 'and':
            tokens = tokens[2:]
        else:
            tokens = tokens[1:]
        check_token(tokens[0], ID)
        check_token(tokens[1], AS)
        tokens = math_or_string_expression(tokens[2:])
    return tokens

def function_call_expression(tokens):
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], ID)
    if tokens[2].isK(WITH):
        return function_arguments(tokens[3:])
    return tokens[2:]

def assignment_expression(tokens):
    check_token(tokens[0],PRONOUN)
    check_token(tokens[1], LETS)
    tokens = tokens[3:] if tokens[2].isK(POSESIVE) else tokens[2:]
    check_token(tokens[0], ID)
    check_token(tokens[1], BE)
    # IDEA: include function call? none return anything anyway
    return math_or_string_expression(tokens[2:])

def sentence(tokens: List[Token]):
    if tokens[1].isK(INCREMENTS):
        return increment_expression(tokens)
    elif tokens[1].isK(DECREASES):
        return decrement_expression(tokens)
    elif tokens[1].isK(SAYS):
        return print_expression(tokens)
    elif tokens[1].isK(ID):
        return function_call_expression(tokens)
    elif tokens[1].isK(LETS):
        return assignment_expression(tokens)

def sentences(tokens: List[Token]):
    tokens = sentence(tokens)
    if tokens[0].isK(DOT):
        return tokens[1:]
    check_token(tokens[0], SEMMI)
    if tokens[1].value() == 'and':
        return sentences(tokens[2:])
    else:
        return sentences(tokens[1:])

def params(tokens: List[Token]):
    check_token(tokens[0], ID)
    while tokens[0].isK(ID):
        # end params
        if tokens[1].isK(SEMMI):
            return tokens[2:]
        check_token(tokens[1], COMMA)
        if tokens[2].value() == 'and':
            tokens = tokens[3:]
        else:
            tokens = tokens[2:]
    return tokens

def method_description(tokens: List[Token]):
    while tokens and tokens[0].isK(TO):
        check_token(tokens[0], TO)
        check_token(tokens[1], ID)
        if tokens[2].isK(PRONOUN) and tokens[3].isK(NEEDS):
            tokens = params(tokens[4:])
            tokens = sentences(tokens)
        else:
            tokens = sentences(tokens[2:])
    return tokens

def class_def(tokens: List[Token]):
    tokens = class_declaration(tokens)
    check_token(tokens[0], DOT)
    tokens = attribute_declaration(tokens[1:])
    tokens = method_declaration(tokens)
    tokens = method_description(tokens)
    return tokens

def classes(tokens: List[Token]):
    tokens = class_def(tokens)
    while tokens and tokens[0].isK(LINE_BREAK):
        tokens = class_def(tokens)
    print(tokens)

class Parser(object):
    def __init__(self, tokens: list, to_ruby=False):
        self.tokens = tokens
        self.text = classes(tokens)
