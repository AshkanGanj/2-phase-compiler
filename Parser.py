import sys
from Lexer import *
from colorama import Fore,Style

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.line = 0
        self.nextToken()
        self.nextToken()

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # match current toke
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort(Fore.LIGHTRED_EX+"Expected " + kind.name +
                       ", got " + self.curToken.kind.name +" in line "+str(self.line))
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit(Fore.LIGHTRED_EX+"Error. " + message + "in line : " + str(self.line))

    # program -> {statement}
    def program(self):
        print(Fore.LIGHTGREEN_EX+"PROGRAM:")
        print(Style.RESET_ALL)
        print("STATEMENT:")
        while not self.checkToken(TokenType.EOF):
            self.statement(4)

    def statement(self,indent):
        # "if" or "if/else"
        if self.checkToken(TokenType.if_ganj):
            print(' ' * indent +"STATEMENT-IF")
            self.nextToken()
            self.match(TokenType.parenthesesOP)
            self.comparison(indent = indent+4)
            self.match(TokenType.parenthesesCL)
            self.match(TokenType.clone)
            self.match(TokenType.bracketsOP)
            while not self.checkToken(TokenType.bracketsCL):
                self.statement(indent = indent+4)
            self.match(TokenType.bracketsCL)
            # "if/else"
            if self.checkToken(TokenType.newline):
                self.nl()
                if self.checkToken(TokenType.else_ganj):
                    print(' ' * indent +"STATEMENT-ELSE")
                    self.nextToken()
                    self.match(TokenType.clone)
                    self.match(TokenType.bracketsOP)
                    while not self.checkToken(TokenType.bracketsCL):
                        self.statement(indent = indent+4)
                    self.match(TokenType.bracketsCL)
                else:
                    pass
            elif self.checkToken(TokenType.else_ganj):
                    print(' ' * indent +"STATEMENT-ELSE")
                    self.nextToken()
                    self.match(TokenType.clone)
                    self.match(TokenType.bracketsOP)
                    while not self.checkToken(TokenType.bracketsCL):
                        self.statement(indent = indent+4)
                    self.match(TokenType.bracketsCL)
            else:
                pass        
        # while
        elif self.checkToken(TokenType.while_ganj):
            print(' ' * indent +"STATEMENT-WHILE")
            self.nextToken()
            self.match(TokenType.parenthesesOP)
            self.comparison(indent = indent+4)
            self.match(TokenType.parenthesesCL)
            self.match(TokenType.clone)
            self.match(TokenType.bracketsOP)
            while not self.checkToken(TokenType.bracketsCL):
                self.statement(indent = indent+4)
            self.match(TokenType.bracketsCL)
        # for
        elif self.checkToken(TokenType.for_ganj):
            print(' ' * indent +"STATEMENT-FOR")
            self.nextToken()
            self.match(TokenType.parenthesesOP)
            self.forStatement(indent = indent+4)
            self.match(TokenType.parenthesesCL)
            self.match(TokenType.clone)
            self.match(TokenType.bracketsOP)
            while not self.checkToken(TokenType.bracketsCL):
                self.statement(indent = indent+4)
            self.match(TokenType.bracketsCL)
        # function
        elif self.checkToken(TokenType.func_ganj):
            print(' ' * indent +"STATEMENT-FUNCTION")
            self.nextToken()
            self.match(TokenType.identifire)
            self.match(TokenType.aquladOP)
            #if we don't have argomanse
            if self.checkToken(TokenType.aquladCL):
                self.nextToken()
                self.match(TokenType.clone)
                self.match(TokenType.bracketsOP)
                while not self.checkToken(TokenType.bracketsCL):
                    self.statement(indent = indent+4)
                self.match(TokenType.bracketsCL)
            else:
                self.argomanse(indent = indent+4)
                self.match(TokenType.clone)
                self.match(TokenType.bracketsOP)
                while not self.checkToken(TokenType.bracketsCL):
                    self.statement(indent = indent+4)
                self.match(TokenType.bracketsCL)
        # call function and assignment
        elif self.checkToken(TokenType.identifire):
            assignindent = self.curToken.text
            self.nextToken()
            if self.checkToken(TokenType.assign):
                print(' ' * (indent) +"identifier : "+Fore.LIGHTBLUE_EX+ str(assignindent))
                print(Style.RESET_ALL)
                print(' ' * indent +"STATEMENT-ASSIGNMENT") 
                self.match(TokenType.assign)
                self.expression(indent = indent)
            elif self.checkToken(TokenType.parenthesesOP):
                self.nextToken()
                if self.checkToken(TokenType.parenthesesCL):
                    print(' ' * indent +"CALL-FUNCTION")
                    self.nextToken()
                else:     
                    self.expression(indent = indent+4)
                    while not self.checkToken(TokenType.parenthesesCL):
                        print(' ' * indent +"CALL-FUNCTION")
                        self.match(TokenType.comma)
                        self.expression(indent = indent+4)
                    self.match(TokenType.parenthesesCL)
        #skip /n
        elif self.checkToken(TokenType.newline):
            self.line +=1
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
        self.nl(indent+4)

    def nl(self,indent):
        # print(' ' * indent + "NEWLINE")
        self.match(TokenType.newline)
        self.line +=1
        while self.checkToken(TokenType.newline):
            self.nextToken()
            self.line +=1
    # comparison --> expression ("<==>" | ">" | "<" ) expression)
    def comparison(self,indent):
        print(' ' * indent +"COMPARISON")
        self.expression(indent = indent+4)
        if self.isComparisonOperator(indent):
            self.nextToken()
            self.expression(indent = indent+4)
        else:
            self.abort(Fore.RED + "Expected comparison operator at: " +
                       self.curToken.text +" in line :"+str(self.line))

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator(indent):
            self.nextToken()
            self.expression(indent = indent+4)

     # Return true if the current token is a comparison operator.
    def isComparisonOperator(self,indent):
        
        if self.checkToken(TokenType.greater) or self.checkToken(TokenType.equal) or self.checkToken(TokenType.smaller):
            print(' ' * (indent+4) +Fore.LIGHTBLUE_EX+"Token "+ str(self.curToken.kind.name))
            print(Style.RESET_ALL)
            return True
        else:
            return False
    # expression --> term {( "-" | "+" ) term}
    def expression(self,indent):
        print(' ' * indent +"EXPRESSION:")
        self.term(indent = indent+4)
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.plus) or self.checkToken(TokenType.minus):
            print(' ' * (indent+4) +Fore.LIGHTBLUE_EX+"Token "+ str(self.curToken.kind.name))
            print(Style.RESET_ALL)
            self.nextToken()
            self.term(indent = indent+4)
    # term --> primar {( "/" | "*" ) primary}
    def term(self,indent):
        print(' ' * indent +"TERM:")
        self.primary(indent = indent+4)
        while self.checkToken(TokenType.mult) or self.checkToken(TokenType.division):
            print(' ' * (indent+4) +Fore.LIGHTBLUE_EX+"Token "+ str(self.curToken.kind.name))
            print(Style.RESET_ALL)
            self.nextToken()
            self.primary(indent = indent+4)
 
     # primary --> number | ident
    def primary(self,indent):
        print(' ' * indent+"PRIMARY : ")
        if self.checkToken(TokenType.number):
            print(' ' * (indent+8) +Fore.YELLOW + str(self.curToken.text))
            print(Style.RESET_ALL)
            self.nextToken()
        elif self.checkToken(TokenType.identifire):
            print(' ' * (indent+8) + Fore.YELLOW +str(self.curToken.text))
            print(Style.RESET_ALL)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text+" in line "+str(self.line))
    #argomanse --> (identifire"comma")*identifire|Lynda 
    def argomanse(self,indent):
        print(' ' * indent +"FUNCTION'S ARGOMANSE")
        print(' ' * (indent+4) +"identifier : "+Fore.LIGHTBLUE_EX+ str(self.curToken.text))
        print(Style.RESET_ALL)
        self.match(TokenType.identifire)
        while not self.checkToken(TokenType.aquladCL):
            self.match(TokenType.comma)
            print(' ' * (indent+4) +"identifier : "+Fore.LIGHTBLUE_EX+ str(self.curToken.text))
            print(Style.RESET_ALL)
            self.match(TokenType.identifire)
        self.match(TokenType.aquladCL)
    #forStatement --> {"identifire" "<=>" expression"comma"expression"comma"comparison}
    def forStatement(self,indent):
        print(' ' * indent +"FOR IN STATEMENT")
        if self.checkToken(TokenType.identifire):
            print(' ' * (indent) +"identifier : "+Fore.LIGHTBLUE_EX+ str(self.curToken.text))
            print(Style.RESET_ALL)
            self.nextToken()
            print(' ' * (indent) +"STATEMENT-ASSIGNMENT") 
            self.match(TokenType.assign)
            self.expression(indent)
            self.match(TokenType.comma)
            self.expression(indent = indent)
            self.match(TokenType.comma)
            self.comparison(indent = indent)
        else:
            self.abort("Unexpected token at " + self.curToken.text+"in line :"+str(self.line))
        