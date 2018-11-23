from keywords import __all__
from Symbol import Sym, ID, STRING

class SymbolTable(object):
    def __init__(self, name: str):
        self.name = name
        self.identifiers = {}

    def lookup(self, value: str):
        lower = value.lower()
        tkn = self.identifiers.get(lower)
        if tkn is not None:
            return tkn
        kwd = __all__.get(lower)
        if kwd is not None:
            return kwd
        if value[0] == '"':
            new_tkn = self.identifiers[value] = Sym(STRING, value)
        else:    
            new_tkn = self.identifiers[value] = Sym(ID, lower)
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
