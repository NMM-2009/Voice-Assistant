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
                    tokens.append(Token(TokenType.NUMBER, float("".join(currentNumber))))
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
        tokens.append(Token(TokenType.NUMBER, float("".join(currentNumber))))
        tokenPosition += 1
        currentNumber = []

    return tokens

precedence = {
    TokenType.PLUS: 1,
    TokenType.MINUS: 1,
    TokenType.TIMES: 2,
    TokenType.DIVIDE: 2,
}

def shuntingYard(tokens):
    output = []
    operator = []
    for token in tokens:
        if token.type == TokenType.NUMBER:
            output.append(token)
        else:
            if token.type == TokenType.LBRACKET:
                operator.append(token)
            else:
                if len(operator) == 0:
                    operator.append(token)
                elif operator[-1].type == TokenType.LBRACKET:
                    operator.append(token)
                elif token.type == TokenType.RBRACKET:
                    while operator[-1].type != TokenType.LBRACKET:
                        output.append(operator.pop())
                    operator.pop()
                elif precedence[token.type] > precedence[operator[-1].type]:
                    operator.append(token)
                else:
                    while (len(operator) > 0 and operator[-1].type != TokenType.LBRACKET and precedence[operator[-1].type] >= precedence[token.type]):
                        output.append(operator.pop())
                    operator.append(token)
                
    numOperators = len(operator)
    for i in range(numOperators):
        output.append(operator.pop())
    
    return output

def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    return a / b

operations = {
    TokenType.PLUS : add,
    TokenType.MINUS : subtract,
    TokenType.TIMES : multiply,
    TokenType.DIVIDE : divide,
}

def calculate(input):
    input = shuntingYard(tokenise(input))
    numbers = []
    for token in input:
        if token.type == TokenType.NUMBER:
            numbers.append(token.value)
        else:
            b = numbers.pop()
            a = numbers.pop()
            numbers.append(operations[token.type](a, b))
    return numbers[0]