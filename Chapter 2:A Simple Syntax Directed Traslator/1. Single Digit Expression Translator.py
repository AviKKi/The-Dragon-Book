'''
    Section 2.5 in book
    
    The given program will turn a in-fix expression to 
    post-fix using a recursive-desent parser with grammer as
    follows -
    expr -> expr + term 
         |  expr - term
         |  term
    term -> 0 | 1 | 2 | ..... | 9

    removing left recursion we have following grammer - 
    expr -> term rest
    rest -> + term rest
         |  - term rest
         |  e
    term -> 0 | 1 | 2 | ..... | 9
'''
from typing import Union


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, string: str):
        self.string = string
        self.index = 0

    def getch(self) -> Union[str, None]:
        ''' 
        return the next character in the string
        and shorten string by first character
        return None if empty string
        '''
        if not self.string:
            return None
        ch = self.string[0]
        self.string = self.string[1:]
        self.index += 1
        return ch

    #######  Parser Functions #########

    def expr(self):
        self.term()
        self.rest()

    def term(self):
        ch = self.getch()
        if ch == None:
            raise ParseError(f"Expected a digit at pos {self.index}")
        if ch in '0123456789':
            print(ch, end="")

    def rest(self):
        ch = self.getch()
        if ch == None:
            return
        if ch in '+-':
            self.term()
            print(ch, end="")
            self.rest()
        else:
            raise ParseError(f"Expected + or - at pos {self.index}")

    ###################################


if __name__ == '__main__':
    while True:
        try:
            parser = Parser(input(">>>"))
            parser.expr()
            print()
        except Exception as e:
            print()
            print(e)
