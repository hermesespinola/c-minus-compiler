from Symbol import Sym, SymEnum

class Token(object):
    def __init__(self, symbol: Sym, line: int, col: int, dtype=None):
        self.symbol = symbol
        self.line = line
        self.col = col
        self.dtype = dtype

    def isK(self, kind):
        return self.symbol.kind is kind

    def inK(self, kindList):
        return self.symbol.kind in kindList

    def value(self):
        return self.symbol.value

    def __repr__(self):
        return '<{}, {}, {}:{}:{}>'.format(
            repr(SymEnum(self.symbol.kind)),
            self.dtype,
            self.symbol.value,
            self.line,
            self.col
        )
