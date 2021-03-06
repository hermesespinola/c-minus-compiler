import string
from Symtable import SymbolTable
from token import Token
from Symbol import Sym, NUM
from keywords import arithmetic_ops, relational_ops, boolean_ops, assignment, punctuation

WHITE = '\n\t\r '
DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
DOT = {'.'}
class Node(object):
    def __init__(self, transitions=None, is_final=False):
        self.transitions = transitions
        self.is_final = is_final

    def move(self, c: str):
        for tran in self.transitions:
            if c in tran[0]:
                return tran[1]
        # TODO: create error with line and column number, or collect all errors and raise them later.
        return None

terminalNode = Node([], is_final=True)
assignmentNode = Node([({ '=' }, terminalNode)], is_final=True)
relationalNode = Node([({ '=' }, terminalNode)], is_final=True)
booleanNode = Node([({ '=' }, terminalNode)], is_final=True)
floatNode = Node(is_final=True)
floatNode.transitions = [(DIGITS, floatNode)]
dotNode = Node([(DIGITS, floatNode)])
intNode = Node(is_final=True)
intNode.transitions = [(DIGITS, intNode), (DOT, dotNode)]
idNode = Node(is_final=True)
idNode.transitions = [(set(string.ascii_letters).union(DIGITS), idNode)]
initialNode = Node([
    (set(arithmetic_ops.keys()), terminalNode),
    (set(relational_ops.keys()), relationalNode),
    (set(boolean_ops.keys()), booleanNode),
    (set(assignment.keys()), assignmentNode),
    (set(punctuation.keys()), terminalNode),
    (set(string.ascii_lowercase), idNode),
    (DIGITS, intNode)
])

def lexException(line: str, lineno: int, col: int):
    import re
    msg = "token no esperado en linea {}, columna {}:\n{}{}" \
        .format(lineno, col, line, re.sub(r'[^\s]', ' ', line[:col]) + '^')
    print(msg)
    exit()

def lstrip(string):
    i = 0
    stripped = { '\t': 0, ' ': 0, '\r': 0, '\n': 0 }
    while len(string) < i and string[i] in WHITE:
        stripped[string[i]] += 1
        i += 1
    return string[i:], stripped, i

def tokenize(line: str, lineno: int, symtable: SymbolTable):
    current = initialNode
    tokens = []
    value = ''
    for col, char in enumerate(line):
        if current is None:
            lexException(line, lineno, col-1)
        if current is initialNode and char in WHITE:
            continue
        nxt = current.move(char)
        if nxt is not None:
            value += char
            current = nxt
        elif current.is_final:
            if current is intNode or current is floatNode:
                tokens.append(Token(Sym(NUM, value), lineno, col))
            else:
                symbol = symtable.lookup(value)
                tokens.append(Token(symbol, lineno, col))
            current = initialNode if char in WHITE else initialNode.move(char)
            value = '' if char in WHITE else char
        else:
            lexException(line, lineno, col)
    if current.is_final:
        if current is intNode or current is floatNode:
            tokens.append(Token(Sym(NUM, value), lineno, col))
        else:
            symbol = symtable.lookup(value)
            tokens.append(Token(symbol, lineno, col))
    return tokens
