'''
    Section 2.7 in book

    This implements a program from Syntax-Directed Translation for given I/O
    input:  { int x; char y; { bool y; x; y; } x; y; }
    output: { { x:int; y:bool; } x:int; y:char; }

    Grammer:

        program -> block
        block -> {
                decls stmts 
                }
        decls -> decls decl 
              -> e
        decl  -> type id ;
        stmts -> stmts stmt
              -> e
        stmt  -> block | id ;

    Removing Left Recursion:
        program -> block
        block -> {
                decls stmts 
                }
        decls -> decl decls 
              -> e
        decl  -> type id ;
        stmts -> stmt stmts
              -> e
        stmt  -> block | id ;
    Note: Code for above translator is not provided in the book, only grammer is given.
'''
from enum import Enum, auto
from typing import List, Union, Tuple, Dict

DATATYPES = {'int', 'bool', 'float', 'char'}
KEYWORDS = set(DATATYPES)


class Token(Enum):
    semicolon = auto()
    opening_curly = auto()
    closing_curly = auto()
    id = auto()
    keyword = auto()


class Lexer:
    def __init__(self, string: str) -> None:
        self.string = string
        self.index = 0
        self.line_no = 0
        # tuple of token type and value
        self.tokens: List[Tuple[Token, str]] = []

    def getch(self) -> Union[str, None]:
        '''
            Return a character at current index and increment the index counter
            if EOF return None
        '''
        if self.index >= len(self.string):
            return None
        self.index += 1
        return self.string[self.index-1]

    def scan(self) -> List[Tuple[Token, str]]:
        ch = self.getch()
        while ch != None:
            if ch in ' \t':
                pass
            elif ch == '\n':
                self.line_no += 1
            elif ch.isalpha() or ch == '_':
                word = ''
                while ch != None and (ch.isalnum() or ch == '_'):
                    word += ch
                    ch = self.getch()
                self.index -= 1
                self.tokens.append(
                    (Token.keyword if word in KEYWORDS else Token.id, word))
            elif ch == ';':
                self.tokens.append((Token.semicolon, ';'))
            elif ch == '{':
                self.tokens.append((Token.opening_curly, '{'))
            elif ch == '}':
                self.tokens.append((Token.closing_curly, '}'))

            else:
                raise Exception(f'unkown character {ch}')
            ch = self.getch()
        return self.tokens


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Tuple[Token, str]]) -> None:
        self.tokens = tokens
        self.index = 0
        self.symbol_table = Env()

    def get_token(self):
        '''
            return current token and increment index
            return None when no more tokens left
        '''
        self.index += 1
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index-1]

    def program(self):
        self.block()

    def block(self):
        token = self.get_token()
        if token[1] == '{':
            print('{ ', end='')
            self.symbol_table.push()
            self.decls()
            self.stmts()
        else:
            raise ParseError(
                'unexpected character, expected a `{` at the end of a block')
        token = self.get_token()
        if token != None and token[1] != '}':
            raise ParseError('unexpected character, expected a `}`')
        print('} ', end='')
        self.symbol_table.pop()

    def decls(self):
        while self.index <= len(self.tokens) and self.tokens[self.index][1] in DATATYPES:
            self.decl()

    def decl(self):
        token = self.get_token()
        if token[1] in DATATYPES:
            datatype = token[1]
            token = self.get_token()
            if token == None or token[0] != Token.id:
                raise ParseError(f'Expected an indentifier')
            identifier = token[1]
            token = self.get_token()
            if token == None or token[1] != ';':
                raise ParseError(f'Expected a semicolon \';\'')
            self.symbol_table[identifier] = datatype
        else:
            raise ParseError(
                f'Unidentiefied datatype {token[1]} expected one of {", ".join(DATATYPES)}')

    def stmts(self):
        while self.index <= len(self.tokens) and self.tokens[self.index][0] == Token.id or self.tokens[self.index][0] == Token.opening_curly:
            self.stmt()

    def stmt(self):
        token = self.get_token()
        if token != None and token[0] == Token.id:
            identifier = token[1]
            token = self.get_token()
            if token != None and token[0] != Token.semicolon:
                raise ParseError("Expected a semicolon")
            print(f'{identifier}: {self.symbol_table[identifier]}; ', end='')
        elif token != None and token[0] == Token.opening_curly:
            self.index -= 1
            self.block()
        else:
            raise ParseError("Expected a '{' or an identified")


class Env:
    '''
        Our Nested Symbol Table
    '''

    def __init__(self) -> None:
        self.tables: List[Dict[str, str]] = [{}]

    def push(self):
        '''
            this will create a copy of symbol table and push on the top of stack
        '''
        self.tables.append(self.tables[-1].copy())

    def pop(self):
        '''
            this will remove the topmost table from the stack
        '''
        self.tables.pop()

    def __setitem__(self, key, item):
        if len(self.tables) == 0:
            raise Exception("No tables")
        self.tables[-1][key] = item

    def __getitem__(self, key):
        if len(self.tables) == 0:
            raise Exception("No tables")
        return self.tables[-1][key]


if __name__ == '__main__':
    while True:
        try:
            lexer = Lexer(input(">>> "))
            parser = Parser(lexer.scan())
            parser.program()
            print()
        except Exception as e:
            print(e)
