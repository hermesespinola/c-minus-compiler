import sys
from lexer import Lexer
from parser import Parser
import fileinput
from fileinput import FileInput
from pprint import pprint

def main(file: FileInput):
    lexer = Lexer(file)
    tkns = lexer.get_tokens()
    parser = Parser(tkns)

if __name__ == '__main__':
    main(fileinput.input())
    fileinput.close()
