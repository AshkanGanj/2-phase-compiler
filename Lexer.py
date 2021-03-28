import sys
import enum

from colorama.ansi import Fore, Style

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.currentChar = ''   # Current character in the string.
        self.currentPos = -1    # Current position in the string.
        self.line = 1
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.currentPos += 1
        if self.currentPos >= len(self.source):
            self.currentChar = '\0'  # EOF
        else:
            self.currentChar = self.source[self.currentPos]

    # Return the lookahead character.
    def peek(self, step):
        if self.currentPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.currentPos+step]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit(Fore.LIGHTRED_EX + "Lexing error. "  +message+" in line "+str(self.line))

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.currentChar == ' ' or self.currentChar == '\t' or self.currentChar == '\r':
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.currentChar == '#':
            while self.currentChar != '\n':
                self.nextChar()
    # Return the next token.

    def getToken(self):
        self.skipWhitespace()
        # self.skipComment()
        token = None
        token = self.checkLexeme()
        self.nextChar()
        return token
    def checkLexeme(self):
        if self.currentChar == '+':
            if self.peek(1) == '+':
                lastChar = self.currentChar
                self.nextChar()
                return Token(lastChar + self.currentChar, TokenType.plus)
            else:
                self.abort("Unknown token: " + self.currentChar)
        elif self.currentChar == '-':
            if self.peek(1) == '-':
                lastChar = self.currentChar
                self.nextChar()
                return Token(lastChar + self.currentChar, TokenType.minus)
            else:
                self.abort("Unknown token: " + self.currentChar)
        elif self.currentChar == '*':
            return Token(self.currentChar, TokenType.mult)
        elif self.currentChar == '/':
            if self.peek(1) == '\\':
                lastChar = self.currentChar
                self.nextChar()
                return Token(lastChar + self.currentChar, TokenType.division)
            else:
                self.abort("Unknown token: " + self.currentChar)
        elif self.currentChar == '.' and self.peek(1).isdigit():
            startPos = self.currentPos
            while self.peek(1).isdigit():
                self.nextChar()
            # Get the substring.
            tokText = self.source[startPos: self.currentPos + 1]
            return Token(tokText, TokenType.number)
        elif self.currentChar == '.':
            return Token(self.currentChar, TokenType.dot)
        elif self.currentChar.isdigit():
            startPos = self.currentPos
            while self.peek(1).isdigit():
                self.nextChar()
            if self.peek(1) == '.': 
                self.nextChar()
                while self.peek(1).isdigit():
                    self.nextChar()
            # Get the substring.
            tokText = self.source[startPos: self.currentPos + 1]
            return Token(tokText, TokenType.number)
        elif self.currentChar == ':':
           return Token(self.currentChar, TokenType.clone)
        elif self.currentChar == ',':
           return Token(self.currentChar, TokenType.comma)
        elif self.currentChar == '<' and self.peek(1) == '=' and self.peek(2)==">":
            self.nextChar()
            self.nextChar()
            return Token(self.currentChar, TokenType.assign)
        elif self.currentChar == '<' and self.peek(1) == '=' and self.peek(2)=="=" and self.peek(3)==">":
            self.nextChar()
            self.nextChar()
            self.nextChar()
            return Token(self.currentChar, TokenType.equal)
        elif self.currentChar == '>':
            return Token(self.currentChar, TokenType.greater)
        elif self.currentChar == '(':
            return Token(self.currentChar, TokenType.parenthesesOP)
        elif self.currentChar == ')':
            return Token(self.currentChar, TokenType.parenthesesCL)
        elif self.currentChar == '[':
            return Token(self.currentChar, TokenType.aquladOP)
        elif self.currentChar == ']':
            return Token(self.currentChar, TokenType.aquladCL)
        elif self.currentChar == '{':
            return Token(self.currentChar, TokenType.bracketsOP)
        elif self.currentChar == '}':
            return Token(self.currentChar, TokenType.bracketsCL)
        elif self.currentChar == '<':
            return Token(self.currentChar, TokenType.smaller)
        # check identifiers
        elif self.currentChar =="g":
            startPos = self.currentPos-1
            if self.peek(1)=="a":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="n":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="j":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="_":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            while self.peek(1).isalnum():
                self.nextChar()
            # Check if the token is in the list of keywords.
            # Get the substring.
            tokText = self.source[startPos: self.currentPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:  # Identifier
                return Token(tokText, TokenType.identifire)          
        # cheking keywords
        elif self.currentChar.isalpha():
            startPos = self.currentPos
            while self.peek(1).isalpha():
                self.nextChar()
            if self.peek(1) =="_":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="g":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="a":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="n":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            if self.peek(1)=="j":
                self.nextChar()
            else:
                self.abort("Unknown token: " + self.currentChar)
            # Check if the token is in the list of keywords.
            # Get the substring.
            tokText = self.source[startPos: self.currentPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword != None:  # keyword
                return Token(tokText, keyword)   
        elif self.currentChar == '\n':
            self.line +=1
            return Token(self.currentChar, TokenType.newline)
        elif self.currentChar == '\0':
            return Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.currentChar)


# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None



class TokenType(enum.Enum):
    EOF = -1 
    newline = 0
    number = 2 
    identifire = 3 
    string = 4
	
    if_ganj = 101
    else_ganj = 102
    while_ganj = 103
    for_ganj = 104
    func_ganj = 105
    
    equal = 201  #<=>
    plus = 202 
    minus = 203
    mult = 204 #*
    division = 205 #//
    assign = 206 # <==>
    smaller = 208 # <
    greater = 209 # >
	
    clone=302 #:
    comma=303
    dot=30
    parenthesesOP=305
    parenthesesCL=306
    bracketsOP = 307
    bracketsCL = 308
    aquladOP = 309 #"["
    aquladCL=310 #"]"
