from keywords import __all__
from Symbol import Sym, ID

class SymbolTable(object):
    def __init__(self, name: str):
        self.name = name
        self.identifiers = {}

    def lookup(self, value: str):
        tkn = self.identifiers.get(value)
        if tkn is not None:
            return tkn
        kwd = __all__.get(value)
        if kwd is not None:
            return kwd
        new_tkn = self.identifiers[value] = Sym(ID, value)
        return new_tkn
    
    def contains(self, value: str):
        tkn = self.identifiers.get(value)
        return tkn is not None

    def get_identifiers(self):
        return self.identifiers.keys()

    def get_symbols(self):
        return self.identifiers.values()

    def print_table(self):
        print(self.identifiers)
    
    def __repr__(self):
        return self.name + ' symtable: ' + self.identifiers.__str__()
