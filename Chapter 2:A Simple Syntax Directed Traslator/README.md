### Summary
This chapter gives a basic summary of how easy it is to construct a basic compiler, you'll be making a very naive parser and lexer to start with, it'll guide you through whole frontend of a compiler before diving deep into those topics in later chapters.

#### Pre-requisite
- Understanding of grammer and production rules
- Understanding of ambiguity in grammer
- Understanding of left and right recursive grammer

#### Explanation of code files
- [1.Single Digit Expression Translator.py](https://github.com/AviKKi/The-Dragon-Book/blob/master/Chapter%202:A%20Simple%20Syntax%20Directed%20Traslator/1.%20Single%20Digit%20Expression%20Translator.py)
  
  Function of this code is to convert a in-fix expression (1+2) into a post-fix expression (12+) given only operators are + and - and operands are only single digit. 
  Parser implemented in this section is a **recursive descent parser**, it is as easy as writing a function for each of the production rule in the grammer and you are done, when starting production will call other production functions recursively based on character/lexeme encountered.
  Compiler you'll be making here is more of a Syntax Directed Translator, what it basically means `parser` is whole :heart: of this compiler, you'll add certain print statements in-between parser's code and viola a code translator is ready.
  Note: unlike a parser in a compiler this doesn't take input from a lexer, but it directly consumes raw string, and also it doesn't produce any intermediate representation for the code parsed.
  
- [2.Lexer.py](https://github.com/AviKKi/The-Dragon-Book/blob/master/Chapter%202:A%20Simple%20Syntax%20Directed%20Traslator/2.Lexer.py)
  
  This is a simple lexer capable of identifying Number, words and other tokens in a code. This is a simple program that scans input string with certain if and else statements, that's the purest essence of a lexer.
  Because hand-coding this is not the best way out there, later we'll learn how **DFA** can be helpful, and after that we'll understand how **Regular Expressions** can make this even more easier.   

- [3.Symbol Table.py](https://github.com/AviKKi/The-Dragon-Book/blob/master/Chapter%202:A%20Simple%20Syntax%20Directed%20Traslator/3.Symbol%20Table.py)
  
  Code for this section is not implemented in the book but a grammer is given, so I implemented it.
  Parser and Lexer are nearly same as previous section, what is new is the `Env` class which supports holding information about identifiers/variables declared in the code along with the support for nesting.
  
