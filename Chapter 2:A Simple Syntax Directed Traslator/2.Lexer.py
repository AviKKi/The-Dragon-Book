'''
    Section 2.6 in book
    Psuedo code

    Token scan(){
        skip white spaces
        handle numbers
        handle reserved words and identifiers
        treat everything left as a token 
    }

    Exercises in section 2.6.6 are implemented in different file
'''


class Lexer:
    def __init__(self, string: str):
        self.string = string
        self.line = 0
        self.line_index = 0
        self.index = 0

    def getch(self) -> str:
        '''
            Return a character at current index and increment the index counter
            if EOF return None
        '''
        if self.index >= len(self.string):
            return None
        self.index += 1
        return self.string[self.index-1]

    def _handle_word(self) -> str:
        '''
            return tuple 
            - identiefier or keyword starting at current index
            - peek character after the word
        '''
        peek = self.string[self.index-1]
        word = peek
        peek = self.getch()

        while peek != None and (peek.isalnum() or peek == '_'):
            word += peek
            peek = self.getch()

        return word, peek

    def scan(self):
        peek = self.getch()
        while peek != None:
            if peek in ' \t':
                continue

            elif peek == '\n':
                self.line += 1
                self.line_index = 0

            elif peek.isnumeric():  # handle numbers
                number = 0
                while peek != None and peek.isnumeric():
                    number = 10*number + int(peek)
                    peek = self.getch()
                print(f"Number: {number}")

            elif peek.isalpha() or peek == '_':
                word, peek = self._handle_word()
                print(f'Word: {word}')

            else:
                print(f'Token: {peek}')
                peek = self.getch()


if __name__ == "__main__":
    while True:
        lexer = Lexer(input(">>>"))
        lexer.scan()
