from FuncSymTable import FunctionSymbolTable
from token import Token
from Symbol import *
from typing import Tuple, Dict, List
from syntax_tree import *
from keywords import data_types

def varNameGenerator():
    i = 1
    while True:
        yield 't' + str(i)
        i += 1
getVarName = varNameGenerator()

def labelNameGenerator():
    i = 1
    while True:
        yield 'L' + str(i)
        i += 1
getLabelName = labelNameGenerator()

def throwSyntaxError(msg):
    raise Exception(msg)

def check_id(token: Token, dtype: int):
    if token.symbol.kind is not ID:
        value = token.symbol.value
        throwSyntaxError('Esperaba identificador pero se encontró: {} en linea {}, columna {} '.format(value, token.line, token.col))
    else:
        token.dtype = dtype

def check_token_type(token: Token, keyword_type):
    if token.symbol.value not in keyword_type:
        value = token.symbol.value
        throwSyntaxError('Esperaba un tipo de dato pero se encontró {} en linea {}, columna {}'.format(value, token.line, token.col))
    return token.symbol.kind

def check_token(token: Token, kind: int):
    if token.symbol.kind is not kind:
        throwSyntaxError('Esperaba {} pero se encontró {} en linea {}, columna {}'.format(SymEnum(kind).name, token.symbol.value, token.line, token.col))

def arguments(start: int, tokens: List[Token]):
    i = start
    eval_text = ''
    params_text = 'begin params\n'
    param_count = 0
    while tokens[i].symbol.kind is not RIGHT_PAR:
        param_count += 1
        i, expression_body, last_operation_text = expression(i, tokens)
        # params text
        var_par = next(getVarName)
        eval_text += expression_body + var_par + ' = ' + last_operation_text + '\n'
        params_text += 'param ' + var_par + '\n'
        if tokens[i].symbol.kind is not COMMA:
            check_token(tokens[i], RIGHT_PAR)
            break
        check_token(tokens[i], COMMA)
        i += 1
    return i, eval_text + params_text, param_count

def call(start, tokens):
    i = start + 2
    text = ''
    n_args = 0
    check_token(tokens[start], ID)
    check_token(tokens[start + 1], LEFT_PAR)
    if not tokens[start + 2].symbol.kind is RIGHT_PAR:
        i, text, n_args = arguments(start + 2, tokens)
    check_token(tokens[i], RIGHT_PAR)
    var_return = next(getVarName)
    text += var_return + ' = ' + 'call ' + tokens[start].symbol.value + ', ' + str(n_args) + '\n'
    return i + 1, text, var_return

def factor(start, tokens):
    if tokens[start].symbol.kind is ID:
        if tokens[start+1].symbol.kind in [SEMMI, RIGHT_BRACKET, RIGHT_PAR]:
            return start + 1, '', tokens[start].symbol.value
        if tokens[start + 1].symbol.kind is LEFT_PAR:
            # function call
            return call(start, tokens)
        elif tokens[start + 1].symbol.kind is LEFT_BRACKET:
            i, body, var_pos = var_array(start, tokens)

            return i, body, '*' + var_pos
        else:
            return start + 1, '', tokens[start].symbol.value
    elif tokens[start].symbol.kind is NUM:
        return start + 1, '', tokens[start].symbol.value
    else:
        check_token(tokens[start], LEFT_PAR)
        i, expr_body, last_operation_text = expression(start + 1, tokens)
        check_token(tokens[i], RIGHT_PAR)
        expr_var = next(getVarName)
        expr_body += expr_var + ' = ' + last_operation_text + '\n'
        return i + 1, expr_body, expr_var

def additive_expression(start, tokens):
    term_end, term_body, term_result = term(start, tokens)
    if tokens[term_end].symbol.kind in [PLUS, MINUS]:
        term2_end, term2_body, term2_result = additive_expression(term_end + 1, tokens)
        term_body += term2_body
        
        term_var = next(getVarName)
        term_body += term_var + ' = ' + term_result.replace('\n', '') + ' ' + tokens[term_end].symbol.value + ' ' + term2_result + '\n'
        term_end = term2_end
        term_result = term_var
    return term_end, term_body, term_result

def term(start, tokens):
    term_end, term_body, term_result = factor(start, tokens)
    if tokens[term_end].symbol.kind in [TIMES, DIV]:
        term2_end, term2_body, term2_result = term(term_end + 1, tokens)
        term_body += term2_body
        
        term_var = next(getVarName)
        term_body += term_var + ' = ' + term_result + ' ' + tokens[term_end].symbol.value + ' ' + term2_result + '\n'
        term_end = term2_end
        term_result = term_var
    return term_end, term_body, term_result

def simple_expression(start, tokens):
    # El de a de veras
    term_end, term_body, term_result = additive_expression(start, tokens)
    if tokens[term_end].symbol.kind in COMPARISON_OPERATORS:
        term2_end, term2_body, term2_result = additive_expression(term_end + 1, tokens)
        term_body += term2_body
        term_var = next(getVarName)
        term_body += term_var + ' = ' + term_result + ' ' + tokens[term_end].symbol.value + ' ' + term2_result + '\n'
        term_end = term2_end
        term_result = term_var
    return term_end, term_body, term_result + '\n'

def var_array(start, tokens):
    check_token(tokens[start + 1], LEFT_BRACKET)
    expression_end, expression_body, last_operation_text = expression(start + 2, tokens)
    check_token(tokens[expression_end], RIGHT_BRACKET)
    var_index = next(getVarName)
    var_offset = next(getVarName)
    text = expression_body + var_index + ' = ' + last_operation_text + '\n'
    text += var_offset + ' = ' + var_index + ' * elem_size(' + tokens[start].symbol.value + ')\n'
    var_pos = next(getVarName)
    text += var_pos + ' = &' + tokens[start].symbol.value + ' + ' + var_offset + '\n'
    return expression_end + 1, text, var_pos

def ass_expression(start, tokens):
    # Check assignment syntax
    i = start
    check_token(tokens[start], ID)
    text, result_var = '', tokens[start].symbol.value
    if tokens[start+1].symbol.kind is LEFT_BRACKET:
         i, var_text, result_var = var_array(start, tokens)
         result_var = '*' + result_var
         text += var_text
    else:
        i += 1
    check_token(tokens[i], ASS)

    if tokens[i+1].symbol.kind is ID and tokens[i+1].symbol.value == 'read':
        check_token(tokens[i+2], LEFT_PAR)
        check_token(tokens[i+3], RIGHT_PAR)
        return i+4, 'read ' + result_var + '\n', result_var
    else:
        i, expr_body_text, last_operation_text = expression(i + 1, tokens)
        text += expr_body_text + result_var + ' = ' + last_operation_text + '\n'
        return i, text, result_var

# Expression can be any of: literal (NUM or BOOL), id, function call, binary expression
def expression(start: int, tokens: List[Token]):
    try:
        return ass_expression(start, tokens)
    except:
        return simple_expression(start, tokens)

def expression_statement(start: int, tokens: List[Token]):
    expr_end, expr_body, _ = expression(start, tokens)
    check_token(tokens[expr_end], SEMMI)
    return expr_end + 1, expr_body 

def while_statement(start: int, tokens: List[Token]):
    # Check while syntax
    check_token(tokens[start], MIENTRAS)
    check_token(tokens[start+1], LEFT_PAR)
    # expression
    expression_end, expr_body_text, last_operation_text = expression(start + 2, tokens)
    while_var = next(getVarName)
    while_label_condition = next(getLabelName)
    while_label_end = next(getLabelName)
    while_text = 'Label ' + while_label_condition + '\n' + expr_body_text + while_var + ' = ' + last_operation_text + '\n'
    while_text += 'if false ' + while_var + ' goto ' + while_label_end  + '\n'

    check_token(tokens[expression_end], RIGHT_PAR)
    # left curl o algo y después statements
    while_body_end = 0
    if tokens[expression_end + 1].symbol.kind is LEFT_CURL:
        while_body_end, while_body_text = func_body(expression_end + 2, tokens)
        while_text += while_body_text
        check_token(tokens[while_body_end], RIGHT_CURL)
        while_body_end += 1
    else:
        while_body_end, while_body_text = statement(expression_end + 1, tokens)
        while_text += while_body_text
    while_text += 'goto ' + while_label_condition + '\n' + 'Label ' + while_label_end
    return while_body_end, while_text
    

def if_statement(start: int, tokens: List[Token]):
    check_token(tokens[start], SI)
    check_token(tokens[start+1], LEFT_PAR)
    # expression
    expression_end, expr_body_text, last_operation_text = expression(start + 2, tokens)
    if_var = next(getVarName)
    if_text = expr_body_text + if_var + ' = ' + last_operation_text + '\n'
    else_label = next(getLabelName)
    end_if_label = next(getLabelName)
    if_text += 'if false ' + if_var + ' goto ' + else_label  + '\n'

    check_token(tokens[expression_end], RIGHT_PAR)
    # left curl o algo y después statements
    if_body_end = 0
    if tokens[expression_end + 1].symbol.kind is LEFT_CURL:
        if_body_end, if_body_text = func_body(expression_end + 2, tokens)
        if_text += if_body_text
        check_token(tokens[if_body_end], RIGHT_CURL)
        if_body_end += 1
    else:
        if_body_end, if_body_text = statement(expression_end + 1, tokens)
        if_text += if_body_text


    # + cosas con los labels
    if_text += 'goto ' + end_if_label + '\n'
    if_text += 'Label ' + else_label + '\n'

    if tokens[if_body_end].symbol.kind is ELSE:
        # else
        if tokens[if_body_end + 1].symbol.kind is LEFT_CURL:
            if_body_end, else_body_text = func_body(if_body_end + 2, tokens)
            if_text += else_body_text
            check_token(tokens[if_body_end], RIGHT_CURL)
            if_body_end += 1
        else:
            if_body_end, else_body_text = statement(if_body_end + 1, tokens)
            if_text += else_body_text

    if_text += 'Label ' + end_if_label + '\n'

    return if_body_end, if_text

def return_statement(start: int, tokens: List[Token]):
    check_token(tokens[start], REGRESA)
    if (tokens[start+1].symbol.kind is SEMMI):
        return start + 2, 'return\n'

    i, expr_body_text, last_operation_text = expression(start + 1, tokens)
    return_var = next(getVarName)
    text = expr_body_text + return_var  + ' = ' + last_operation_text + '\n' + 'return ' + return_var + '\n'
    check_token(tokens[i], SEMMI)
    return i + 1, text

def statement(start: int, tokens: List[Token]):
    kind = tokens[start].symbol.kind
    if kind is SI:
        return if_statement(start, tokens)
    if kind is MIENTRAS:
        return while_statement(start, tokens)
    if kind is REGRESA:
        return return_statement(start, tokens)
    if kind is ID and tokens[start].symbol.value == 'write':
        check_token(tokens[start+1], LEFT_PAR)
        expression_end, expr_body_text, last_operation_text = expression(start + 2, tokens)
        stmt_text = expr_body_text + 'write ' + last_operation_text + '\n'
        check_token(tokens[expression_end], RIGHT_PAR)
        check_token(tokens[expression_end+1], SEMMI)
        return expression_end+2, stmt_text
    else:
        return expression_statement(start, tokens)

def func_body(start: int, tokens: List[Token]):
    i = start
    body_text = ''
    while tokens[i].symbol.kind in STATEMENTS:
        i, statement_text = statement(i, tokens)
        body_text += statement_text
    return i, body_text

def func_declarations(start: int, tokens: List[Token]):
    i = start
    while tokens[i].symbol.kind in DATA_TYPES:
        i = var_def(i, tokens, False)
    return i

def parameters(start: int, tokens: List[Token]):
    i = start
    if tokens[i].symbol.kind is VOID:
        check_token(tokens[i + 1], RIGHT_PAR)
        return i + 2
    if tokens[i].symbol.kind is RIGHT_PAR:
        return i + 1
    while tokens[i-1].symbol.kind is not RIGHT_PAR:
        i = var_def(i, tokens, True)
    return i

def func_def(start: int, tokens: List[Token]):
    text = 'entry ' + tokens[start + 1].symbol.value  + '\n'
    # Check function args
    check_token(tokens[start+2], LEFT_PAR)
    end_args = parameters(start+3, tokens)

    # Check declarations
    check_token(tokens[end_args], LEFT_CURL)
    end_declarations = end_args + 1
    if tokens[end_declarations].symbol.kind in DATA_TYPES:
        end_declarations = func_declarations(end_declarations, tokens)

    # Check function body
    end_body, body_text = func_body(end_declarations, tokens)
    text += body_text
    check_token(tokens[end_body], RIGHT_CURL)
    return end_body + 1, text

def var_def(i, tokens, isParam):
    if tokens[i + 2].symbol.kind is LEFT_BRACKET:
        return i + 6 - isParam
    else:
        return i + 3

def func_defs_var_def(tokens: List[Token]):
    i = 0
    text = ''
    while (i + 2) < len(tokens):
        if tokens[i + 2].symbol.kind in [SEMMI, LEFT_BRACKET]:
            i = var_def(i, tokens, False)
        else:
            i, _text = func_def(i, tokens)
            text += _text
    return i, text

def archivo(tokens: List[Token]):
    last, text = func_defs_var_def(tokens)
    return text

class Parser(object):
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.text = archivo(tokens)
        print(self.text)
