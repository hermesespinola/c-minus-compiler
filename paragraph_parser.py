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
    text = "class " + tokens[1].value().capitalize() + "\n"
    return tokens[5:], text

def factor(tokens):
    if tokens[0].isK(ID) or tokens[0].isK(NUM):
        return tokens[1:]
    elif tokens[0].isK(POSESIVE):
        check_token(tokens[1], ID)
        return tokens[2:]
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

def relop(tokens):
    """
    consumes strings with this form:
    [not] (less|<|greater|>|equal|==|equals|!=) [than|to]
    """
    if tokens[0].isK(NOT):
        tokens = tokens[1:]
    if not tokens[0].inK(COMPARISON_OPERATORS):
        throwSyntaxError('expected comparisson operator')
    if tokens[1].inK([THAN, TO]):
        return tokens[2:]
    return tokens[1:]

def simple_expression(tokens):
    # El de a de veras
    tokens = additive_expression(tokens)
    if tokens[0].inK(COMPARISON_OPERATORS):
        tokens = additive_expression(tokens[1:])
    elif tokens[0].isK(IS):
        tokens = relop(tokens[1:])
        tokens = additive_expression(tokens)
    return tokens

def math_or_string_expression(tokens):
    if tokens[0].isK(STRING):
        text = tokens[0].value()
        return tokens[1:], text
    else:
        after_expression_tokens = simple_expression(tokens)
        i, text = 0, ""
        while tokens[i] is not after_expression_tokens[0]:
            text += str(tokens[i].value()) + " "
            i += 1
        return after_expression_tokens, text

def attribute(tokens: List[Token]):
    text = ""
    # init and assign
    check_token(tokens[0], ID)
    text += tokens[0].value()
    if tokens[1].isK(EQUALS):
        check_token(tokens[2], TO)
        tokens, expression_text = math_or_string_expression(tokens[3:])
        text += ": " + expression_text
        return tokens, text
    else:
        return tokens[1:], text

def attribute_declaration(tokens: List[Token]):
    check_token(tokens[0], PRONOUN)
    first = True
    header_text = "def initialize("
    text = ""
    if not tokens[1].isK(HAS):
        full_text = header_text + ")\n" + text + "end\n"
        return tokens, full_text
    tokens = tokens[2:]
    while tokens[0].isK(ID):
        if first:
            first = False
        else:
            header_text += ", "
        text += "@" + tokens[0].value() + " = " + tokens[0].value() + "\n"
        tokens, attribute_text = attribute(tokens)
        header_text += attribute_text
        # end attribute declarations
        if tokens[0].isK(DOT):
            full_text = header_text + ")\n" + text + "end\n"
            return tokens[1:], full_text
        check_token(tokens[0], COMMA)
        if tokens[1].value() == 'and':
            tokens = tokens[2:]
        else:
            tokens = tokens[1:]
    full_text = header_text + ")\n" + text + "end\n"
    return tokens, full_text

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
    after_expression_tokens, expression_text = math_or_string_expression(tokens[2:])
    text = "puts " + expression_text + "\n"
    return after_expression_tokens, text

def decrement_expression(tokens):
    text = ""
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], DECREASES)
    if tokens[2].isK(POSESIVE):
        tokens = tokens[3:]
        text += "@"
    else:
        tokens = tokens[2:]
    check_token(tokens[0], ID)
    text += tokens[0].value()
    check_token(tokens[1], BY)
    check_token(tokens[2], NUM)
    text += " -= " + str(tokens[2].value()) + "\n"
    return tokens[3:], text

def increment_expression(tokens):
    text = ""
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], INCREMENTS)
    if tokens[2].isK(POSESIVE):
        tokens = tokens[3:]
        text += "@"
    else:
        tokens = tokens[2:]
    check_token(tokens[0], ID)
    text += tokens[0].value()
    check_token(tokens[1], BY)
    check_token(tokens[2], NUM)
    text += " += " + str(tokens[2].value()) + "\n"
    return tokens[3:], text

def function_arguments(tokens):
    text = ""
    check_token(tokens[0], ID)
    text += tokens[0].value() + ": "
    check_token(tokens[1], AS)
    tokens, expression_text = math_or_string_expression(tokens[2:])
    text += expression_text
    while tokens[0].isK(COMMA):
        if tokens[1].value() == 'and':
            if tokens[3].isK(AS):
                check_token(tokens[2], ID)
                text += ", " + tokens[2].value()
                tokens, expression_text = math_or_string_expression(tokens[4:])
                text += ": " + expression_text
            else:
                return tokens, text
        else:
            if tokens[2].isK(AS):
                check_token(tokens[1], ID)
                text += ", " + tokens[1].value()
                tokens, expression_text = math_or_string_expression(tokens[3:])
                text += ": " + expression_text
            else:
                return tokens, text
    return tokens, text

def function_call_expression(tokens):
    text = ""
    check_token(tokens[0], PRONOUN)
    check_token(tokens[1], ID)
    text += tokens[1].value() + "("
    if tokens[2].isK(WITH):
        after_arguments_tokens, arguments_text = function_arguments(tokens[3:])
        text += arguments_text + ")\n"
        return after_arguments_tokens, text
    text += ")\n"
    return tokens[2:], text

def assignment_expression(tokens):
    text = ""
    check_token(tokens[0],PRONOUN)
    check_token(tokens[1], LETS)
    if tokens[2].isK(POSESIVE):
        text += "@"
    tokens = tokens[3:] if tokens[2].isK(POSESIVE) else tokens[2:]
    check_token(tokens[0], ID)
    text += tokens[0].value()
    check_token(tokens[1], BE)
    # IDEA: include function call? none return anything anyway
    after_expression_tokens, expression_text = math_or_string_expression(tokens[2:])
    text += " = " + expression_text + "\n"
    return after_expression_tokens, text


def inner_sentences(tokens):
    text = ""
    tokens, sentence_text = sentence(tokens)
    text += sentence_text
    if tokens[0].isK(DOT):
        return tokens, text
    if tokens[0].isK(SEMMI):
        return tokens, text
    check_token(tokens[0], COMMA)
    if tokens[1].value() == 'and':
        return inner_sentences(tokens[2:])
    else:
        return inner_sentences(tokens[1:])

def conditional_expression(tokens):
    check_token(tokens[0], IF)
    # TODO: Add booleans (TRUE, FALSE) and boolean operators (and, or, not)
    tokens, expression_text = math_or_string_expression(tokens[1:])
    text = "if " + expression_text + "\n"
    tokens, inner_text = inner_sentences(tokens)
    return tokens, text + inner_text

def loop_expression(tokens):
    check_token(tokens[0], WHILE)
    text = "while "
    # TODO: Add booleans (TRUE, FALSE) and boolean operators (and, or, not)
    tokens, expression_text = math_or_string_expression(tokens[1:])
    text += expression_text + "\n"
    after_inner_tokens, inner_text = inner_sentences(tokens)
    text += inner_text + "end\n"
    return  after_inner_tokens, text

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
    elif tokens[0].isK(IF):
        return conditional_expression(tokens)
    elif tokens[0].isK(WHILE):
        return loop_expression(tokens)

def sentences(tokens: List[Token]):
    tokens, sentence_text = sentence(tokens)
    if tokens[0].isK(DOT):
        return tokens[1:], sentence_text
    check_token(tokens[0], SEMMI)
    if tokens[1].value() == 'and':
        after_sentences_tokens, sentences_text = sentences(tokens[2:])
        return after_sentences_tokens, sentence_text + sentences_text
    else:
        after_sentences_tokens, sentences_text = sentences(tokens[1:])
        return after_sentences_tokens, sentence_text + sentences_text

def params(tokens: List[Token]):
    text = ""
    check_token(tokens[0], ID)
    first = True
    while tokens[0].isK(ID):
        # end params
        if not first:
            text += ", "
        else:
            first = False
        text += str(tokens[0].value()) + ":"
        if tokens[1].isK(SEMMI):
            return tokens[2:], text
        check_token(tokens[1], COMMA)
        if tokens[2].value() == 'and':
            tokens = tokens[3:]
        else:
            tokens = tokens[2:]
    return tokens, text

def method_description(tokens: List[Token]):
    text = ""
    while len(tokens) > 0 and tokens[0].isK(TO):
        check_token(tokens[0], TO)
        check_token(tokens[1], ID)
        text += "def " + str(tokens[1].value()) + "("
        if tokens[2].isK(PRONOUN) and tokens[3].isK(NEEDS):
            tokens, params_text = params(tokens[4:])
            text += params_text + ")\n"
            tokens, sentences_text = sentences(tokens)
            text += sentences_text
            text += "end\n"
        else:
            text += ")\n"
            tokens, sentences_text = sentences(tokens[2:])
            text += sentences_text
            text += "end\n"
    return tokens, text

def class_def(tokens: List[Token]):
    tokens, class_declaration_text = class_declaration(tokens)
    check_token(tokens[0], DOT)
    tokens, attribute_declaration_text = attribute_declaration(tokens[1:])
    tokens = method_declaration(tokens)
    tokens, method_description_text = method_description(tokens)
    text = class_declaration_text + attribute_declaration_text + method_description_text
    return tokens, text

def classes(tokens: List[Token]):
    text = ""
    tokens, class_text = class_def(tokens)
    text += class_text
    while tokens and tokens[0].isK(LINE_BREAK):
        class_text = ""
        tokens, class_text = class_def(tokens)
        text += class_text
    print("Text =\n", text)
    return text

class Parser(object):
    def __init__(self, tokens: list, to_ruby=False):
        self.tokens = tokens
        self.text = classes(tokens)
