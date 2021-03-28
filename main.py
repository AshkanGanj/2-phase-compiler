# impelemented by Ashkan ganj
# Github:https://github.com/Ashkan-Agc
from Lexer import *
from Parser import *
import sys
from colorama import Fore,Style


def main():
    print(Fore.LIGHTGREEN_EX+"""
        #################################################
        #               Ashkan Ganj                     #
        #             Compiler project                  #
        #   Parser implemented  with Recursive method   #    
        #   All Dfa and Grammers impelemented manually    #
        #   with out using libraries.                   #
        #   Github:https://github.com/Ashkan-Agc        #
        #################################################   
    """)
    print(Style.RESET_ALL)
    # # read from files
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()
    # source = str(input("Enter : "))
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print(Fore.LIGHTGREEN_EX+"Parsing completed .")
    print(Style.RESET_ALL)

if __name__ == '__main__':
    main()