from keywords import __all__
from token import Token
from typing import Dict, Iterable

class FunctionSymbolTable(object):
    identifiers: Dict[str, Token] = None
    def __init__(self, name: str, dtype: int):
        self.name = name
        self.identifiers = {}
        self.dtype: int = dtype

    def put(self, token: Token):
        retrieved = self.identifiers.get(token.symbol.value)
        # if retrieved is not None:
        #     print('Identificar ya definido: {}'.format(retrieved.symbol.value))
        #     exit()
        self.identifiers[token.symbol.value] = token

    def get_token(self, value) -> Token:
        return self.identifiers.get(value)

    def contains(self, value: str) -> bool:
        tkn = self.identifiers.get(value)
        return tkn is not None

    def get_identifiers(self) -> Iterable[str]:
        return self.identifiers.keys()

    def get_tokens(self) -> Iterable[Token]:
        return self.identifiers.values()

    def print_table(self):
        print(self.identifiers)
    
    def __repr__(self):
        return self.name + ' symtable: ' + self.identifiers.__str__()
