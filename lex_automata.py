import string
from Symtable import SymbolTable
from token import Token
from Symbol import Sym, NUM, LINE_BREAK
from keywords import arithmetic_ops, relational_ops, boolean_ops, assignment, punctuation

DOT = {'.'}
class Node(object):
    def __init__(self, transitions=None, is_final=False):
        self.transitions = transitions
        self.is_final = is_final

    def move(self, c: str):
        for tran in self.transitions:
            if c in tran[0]:
                return tran[1]
        return None

# A class that return True for all expression like: key in everything
# Useful for string automata
class Everything(object):
    def __contains__(self, key):
        return True

terminalNode = Node([], is_final=True)
assignmentNode = Node([({ '=' }, terminalNode)], is_final=True)
relationalNode = Node([({ '=' }, terminalNode)], is_final=True)
booleanNode = Node([({ '=' }, terminalNode)], is_final=True)
floatNode = Node(is_final=True)
floatNode.transitions = [(set(string.digits), floatNode)]
dotNode = Node([(set(string.digits), floatNode)])
intNode = Node(is_final=True)
intNode.transitions = [(set(string.digits), intNode), (DOT, dotNode)]
idNode = Node(is_final=True)
idNode.transitions = [(set(string.ascii_letters+'_').union(string.digits), idNode)]
stringNode = Node(is_final=True)
stringNode.transitions = [('"', terminalNode), (Everything(), stringNode)]
initialNode = Node([
    (set(arithmetic_ops.keys()), terminalNode),
    (set(relational_ops.keys()), relationalNode),
    (set(boolean_ops.keys()), booleanNode),
    (set(assignment.keys()), assignmentNode),
    (set(punctuation.keys()), terminalNode),
    (set(string.ascii_letters), idNode),
    (set(string.digits), intNode),
    ('"', stringNode),
])

def lexException(line: str, lineno: int, col: int):
    import re
    msg = "token no esperado en linea {}, columna {}:\n{}{}" \
        .format(lineno, col, line, re.sub(r'[^\s]', ' ', line[:col]) + '^')
    raise Exception(msg)
    exit()

def lstrip(estring):
    i = 0
    stripped = { '\t': 0, ' ': 0, '\r': 0, '\n': 0 }
    while len(estring) < i and estring[i] in string.whitespace:
        stripped[estring[i]] += 1
        i += 1
    return estring[i:], stripped, i

def tokenize(line: str, lineno: int, symtable: SymbolTable):
    current = initialNode
    tokens = []
    value = ''
    if line == '\n':
        return [Token(Sym(LINE_BREAK, '\n'), lineno, 0)]
    for col, char in enumerate(line):
        if current is None:
            lexException(line, lineno, col-1)
        if current is initialNode and char in string.whitespace:
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
            current = initialNode if char in string.whitespace else initialNode.move(char)
            value = '' if char in string.whitespace else char
        else:
            lexException(line, lineno, col)
    if current.is_final:
        if current is intNode or current is floatNode:
            tokens.append(Token(Sym(NUM, value), lineno, col))
        else:
            symbol = symtable.lookup(value)
            tokens.append(Token(symbol, lineno, col))
    return tokens
