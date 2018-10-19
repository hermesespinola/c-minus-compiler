from fileinput import FileInput
from Symtable import SymbolTable
from lex_automata import tokenize

class Lexer(object):
    def __init__(self, source: FileInput):
        self.source = source
        self.firstLine = source.readline()
        self.table = SymbolTable(source.filename())

    def get_tokens(self):
        firstLineTokens = tokenize(self.firstLine, 1, self.table)
        restTokens = [tkn for line in self.source for tkn in tokenize(line, self.source.lineno(), self.table)]
        return firstLineTokens + restTokens

    def get_symtable(self):
        return self.table
