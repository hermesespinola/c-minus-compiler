from FuncSymTable import FunctionSymbolTable
from token import Token
from Symbol import *
from typing import Tuple, Dict
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
    print(msg)
    print('incorrecto')
    exit()

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

def parameters(start: int, tokens: List[Token]):
    i = start
    parameters_tree = []
    while tokens[i].symbol.kind is not RIGHT_PAR:
        check_id(tokens[i], ID)
        token = func_symtable.get_token(tokens[i].symbol.value)
        dtype = None if token is None else token.dtype
        parameters_tree.append(IdNode(dtype, token.symbol.value))
        if tokens[i+1].symbol.kind is RIGHT_PAR:
            return i + 1, ParametersNode(parameters_tree)
        check_token(tokens[i+1], COMMA)
        check_token(tokens[i+2], ID)
        i += 2
    return i, ParametersNode(parameters_tree)

# Expression can be any of: literal (NUM or BOOL), id, function call, binary expression
def expression(start: int, tokens: List[Token]):
    i = start
    expr_body_text, last_operation_text = 'body\n', 'last'
    while tokens[i].symbol.kind not in [SEMMI, RIGHT_PAR]:
        i += 1
    return i, expr_body_text, last_operation_text
    i = start
    previous = None
    stack = []
    while tokens[i].symbol.kind is not SEMMI:
        # first construct literals, ids and function call tokens
        sym = tokens[i].symbol
        if sym.kind in LITERALS:
            # Check previous node is ok
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is ID:
            nextKind = tokens[i+1].symbol.kind
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            if nextKind is LEFT_PAR:
                # Create function call node with parameters
                i, parameters_node = parameters(i + 2, tokens, func_symtable)
                check_token(tokens[i], RIGHT_PAR)
                stack.append(FuncCallNode(sym.value, parameters_node))
            else:
                token = func_symtable.get_token(sym.value)
                dtype = None if token is None else token.dtype
                stack.append(IdNode(dtype, sym.value))
        elif sym.kind in OPERATORS:
            if previous is None or (previous not in LITERALS and previous is not ID and previous is not RIGHT_PAR):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is LEFT_PAR:
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is RIGHT_PAR:
            if previous is None or (previous not in LITERALS and previous is not ID and previous is not RIGHT_PAR):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            nested_expr = []
            x = stack.pop()
            while x.symbol.kind is not LEFT_PAR if type(x) is Token else True:
                nested_expr.append(x)
                if len(stack) == 0:
                    throwSyntaxError('Sintaxis invalida: falta parentesis izquierdo')
                x = stack.pop()
            stack.append(nested_expr)
        elif sym.kind is SEMMI:
            break
        else:
            throwSyntaxError('Sintaxis invalida: {} en linea {}, columna {}'.format(tokens[i].symbol.value, tokens[i].line, tokens[i].col))
        previous = sym.kind
        i += 1

    # Check balanced parenthesis
    for item in stack:
        if type(item) is Token and item.symbol.kind is LEFT_PAR:
            throwSyntaxError('Sintaxis invalida: parentesis no balanceados en linea {}, columna {}'.format(item.symbol.value, item.line, item.col))

    # TODO: parse intermediate stack to prefix expression
    expression_node = stack
    check_token(tokens[i], SEMMI)
    return i, expression_node

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

def ass_statement(start: int, tokens: List[Token]):
    # Check assignment syntax
    check_token(tokens[start], ID)
    check_token(tokens[start+1], ASS)

    i, expr_body_text, last_operation_text = expression(start + 2, tokens)
    text = expr_body_text + tokens[start].symbol.value  + ' = ' + last_operation_text + '\n'
    check_token(tokens[i], SEMMI)
    return i + 1, text

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
    if kind is ID:
        return ass_statement(start, tokens)
    if kind is REGRESA:
        return return_statement(start, tokens)

def func_body(start: int, tokens: List[Token]):
    i = start
    body_text = ''
    while tokens[i].symbol.kind in STATEMENTS:
        i, statement_text = statement(i, tokens)
        body_text += statement_text
    return i, body_text

def func_declarations(start: int, tokens: list):
    i = start
    while tokens[i].symbol.kind in DATA_TYPES:
        i = var_def(i, tokens)
    return i

def args_def(start: int, tokens: list):
    i = start
    if tokens[i].symbol.kind is VOID:
        check_token(tokens[i + 1], RIGHT_PAR)
        return i + 2
    if tokens[i].symbol.kind is RIGHT_PAR:
        return i + 1
    while tokens[i-1].symbol.kind is not RIGHT_PAR:
        i = var_def(i, tokens)
    return i

def func_def(start: int, tokens: list):
    text = 'entry ' + tokens[start + 1].symbol.value  + '\n'
    # Check function args
    check_token(tokens[start+2], LEFT_PAR)
    end_args = args_def(start+3, tokens)

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

def var_def(i, tokens):
    if tokens[i + 2].symbol.kind is LEFT_BRACKET:
        return i + 6
    else:
        return i + 3

def func_defs_var_def(tokens: list):
    i = 0
    text = ''
    while (i + 2) < len(tokens):
        if tokens[i + 2].symbol.kind in [SEMMI, LEFT_BRACKET]:
            i = var_def(i, tokens)
        else:
            i, _text = func_def(i, tokens)
            text += _text
    return i, text

def archivo(tokens: list):
    last, text = func_defs_var_def(tokens)
    return text

class Parser(object):
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.text = archivo(tokens)
        print(self.text)
