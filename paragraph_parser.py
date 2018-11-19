from FuncSymTable import FunctionSymbolTable
from token import Token
from Symbol import *
from typing import Tuple, Dict, List
from syntax_tree import *

def throwSyntaxError(msg):
    raise Exception(msg)

def check_id(token: Token, dtype: int):
    if not token.isK(ID):
        value = token.value()
        throwSyntaxError('Esperaba identificador pero se encontró: {} en linea {}, columna {} '.format(value, token.line, token.col))
    else:
        token.dtype = dtype

def check_token_type(token: Token, keyword_type):
    if token.value() not in keyword_type:
        value = token.value()
        throwSyntaxError('Esperaba un tipo de dato pero se encontró {} en linea {}, columna {}'.format(value, token.line, token.col))
    return token.symbol.kind

def check_token(token: Token, kind: int):
    if token.isK(not kind):
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

def class_def(tokens: List[Token]):
    tokens = class_declaration(tokens)
    check_token(tokens[0], DOT)
    tokens = attribute_declaration(tokens[1:])
    tokens = method_declaration(tokens)
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
