# Inputs will be from both written and spoken so may be given in words. word2number library will be used to give everything in an easier format

from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    TIMES = 4
    DIVIDE = 5
    LBRACKET = 6
    RBRACKET = 7

    # When getting the type name, it'll give NUMBER and not TokenType.NUMBER for example
    def __str__(self):
        return self.name

class Token:
    def __init__(self, type, value = None):
        self.type = type
        if value != None:
            self.value = value

def tokenise(input):
    tokenPosition = -1
    tokens = []
    currentNumber = []
    for character in input:
        try:
            if character != ".":
                number = int(character)
                currentNumber.append(character)
            else:
                currentNumber.append(".")
        except:
            if character == " ":
                continue
            else:
                if len(currentNumber) > 0:
                    tokens.append(Token(TokenType.NUMBER, "".join(currentNumber)))
                    tokenPosition += 1
                    currentNumber = []
                match character:
                    case "+":
                        tokens.append(Token(TokenType.PLUS))
                        tokenPosition += 1
                    case "-":
                        if tokens != []:
                            if tokens[tokenPosition].type == TokenType.NUMBER or tokens[tokenPosition].type == TokenType.RBRACKET:
                                tokens.append(Token(TokenType.MINUS))
                                tokenPosition += 1
                            else:
                                currentNumber.append("-")
                        else:
                            currentNumber.append("-")
                    case "*":
                        tokens.append(Token(TokenType.TIMES))
                        tokenPosition += 1
                    case "/":
                        tokens.append(Token(TokenType.DIVIDE))
                        tokenPosition += 1
                    case "(":
                        tokens.append(Token(TokenType.LBRACKET))
                        tokenPosition += 1
                    case ")":
                        tokens.append(Token(TokenType.RBRACKET))
                        tokenPosition += 1
    
    # Will always end with a number so add it to tokens
    if len(currentNumber) > 0:
        tokens.append(Token(TokenType.NUMBER, "".join(currentNumber)))
        tokenPosition += 1
        currentNumber = []

    return tokens