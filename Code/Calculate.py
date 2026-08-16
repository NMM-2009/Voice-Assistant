# Inputs will be from both written and spoken so may be given in words. word2number library will be used to give everything in an easier format
# Needs to add unit conversion
# Maybe add vectors

import math
import re
import TTS
from word2number import w2n
from enum import Enum
from State import state

# Logarithms written as "log(value base)"

class TokenType(Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    TIMES = 4
    DIVIDE = 5
    LBRACKET = 6
    RBRACKET = 7
    POWER = 8
    SIN = 9
    COS = 10
    TAN = 11
    LOG = 12
    PERCENT = 13

    # When getting the type name, it'll give NUMBER and not TokenType.NUMBER for example
    def __str__(self):
        return self.name

class Token:
    def __init__(self, type, value = None):
        self.type = type
        if value != None:
            self.value = value

functions = {
    "sin" : TokenType.SIN,
    "cos" : TokenType.COS,
    "tan" : TokenType.TAN,
    "log" : TokenType.LOG,
}

def tokenise(input):
    tokenPosition = -1
    tokens = []
    currentNumber = []
    currentFunction = []
    for character in input:
        try:
            if character != ".":
                number = int(character)
                currentNumber.append(character)
            else:
                currentNumber.append(".")
            currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
        except:
            if character == " ":
                currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                if len(currentNumber) > 0:
                    tokens.append(Token(TokenType.NUMBER, float("".join(currentNumber))))
                    tokenPosition += 1
                    currentNumber = []
            else:
                if len(currentNumber) > 0:
                    tokens.append(Token(TokenType.NUMBER, float("".join(currentNumber))))
                    tokenPosition += 1
                    currentNumber = []
                match character:
                    case "+":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.PLUS))
                        tokenPosition += 1
                    case "-":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        if tokens != []:
                            if tokens[tokenPosition].type == TokenType.NUMBER or tokens[tokenPosition].type == TokenType.RBRACKET:
                                tokens.append(Token(TokenType.MINUS))
                                tokenPosition += 1
                            else:
                                currentNumber.append("-")
                        else:
                            currentNumber.append("-")
                    case "*":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.TIMES))
                        tokenPosition += 1
                    case "/":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.DIVIDE))
                        tokenPosition += 1
                    case "(":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.LBRACKET))
                        tokenPosition += 1
                    case ")":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.RBRACKET))
                        tokenPosition += 1
                    case "^":
                        currentFunction, tokens, tokenPosition = emptyFunction(currentFunction, tokens, tokenPosition)
                        tokens.append(Token(TokenType.POWER))
                        tokenPosition += 1
                    case "%":
                        # No emptyFunction() since % can only ever follow a number
                        tokens.append(Token(TokenType.PERCENT))
                        tokenPosition += 1

                    case _:
                        currentFunction.append(character)

    # Will always end with a number so add it to tokens
    if len(currentNumber) > 0:
        tokens.append(Token(TokenType.NUMBER, float("".join(currentNumber))))
        tokenPosition += 1
        currentNumber = []

    return tokens

def emptyFunction(currentFunction, tokens, tokenPosition):
    while len(currentFunction) >= 3:
        word = ""
        for letter in currentFunction:
            word += letter
        if word in functions:
            tokens.append(Token(functions[word]))
            tokenPosition += 1
            break
        else:
            currentFunction.pop(0)
    return [], tokens, tokenPosition

precedence = {
    TokenType.PLUS: 1,
    TokenType.MINUS: 1,
    TokenType.TIMES: 2,
    TokenType.DIVIDE: 2,
    TokenType.POWER: 3,
}

functionTypes = [
    TokenType.SIN,
    TokenType.COS,
    TokenType.TAN,
    TokenType.LOG,
]

def shuntingYard(tokens):
    output = []
    operator = []
    for token in tokens:
        if token.type == TokenType.NUMBER:
            output.append(token)
        else:
            if token.type == TokenType.PERCENT:
                output.append(token)
            elif token.type == TokenType.LBRACKET or token.type in functionTypes:
                operator.append(token)
            else:
                if len(operator) == 0:
                    operator.append(token)
                elif token.type == TokenType.RBRACKET:
                    while operator[-1].type != TokenType.LBRACKET:
                        output.append(operator.pop())
                    operator.pop()

                    # Scenerios like (30) where no operator would be left in stack
                    try:
                        if operator[-1].type in functionTypes:
                            output.append(operator.pop())
                    except:
                        pass
                elif operator[-1].type == TokenType.LBRACKET:
                    operator.append(token)
                elif operator[-1].type == TokenType.POWER and precedence[token.type] == precedence[operator[-1].type]:
                    operator.append(token)
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
def power(a, b):
    return a ** b
def sin(a):
    return round(math.sin(math.radians(a)), 10)
def cos(a):
    return round(math.cos(math.radians(a)), 10)
def tan(a):
    return round(math.tan(math.radians(a)), 10)
def log(a, b = None):
    if b == None:
        return math.log(a)
    else:
        return math.log(a, b)
def percent(a):
    return a / 100

operations = {
    TokenType.PLUS : add,
    TokenType.MINUS : subtract,
    TokenType.TIMES : multiply,
    TokenType.DIVIDE : divide,
    TokenType.POWER : power,
    TokenType.SIN : sin,
    TokenType.COS : cos,
    TokenType.TAN : tan,
    TokenType.LOG : log,
    TokenType.PERCENT : percent,
}

singleInput = [
    TokenType.SIN,
    TokenType.COS,
    TokenType.TAN,
    TokenType.PERCENT,
]

def calculate(input):
    input = shuntingYard(tokenise(input))
    numbers = []
    for token in input:
        if token.type == TokenType.NUMBER:
            numbers.append(token.value)
        elif token.type in singleInput:
            a = numbers.pop()
            numbers.append(operations[token.type](a))

        # Check for log(8)
        elif len(numbers) == 1 and token.type == TokenType.LOG:
            a = numbers.pop()
            numbers.append(operations[token.type](a))
        else:
            b = numbers.pop()
            a = numbers.pop()
            numbers.append(operations[token.type](a, b))
    TTS.speak(str(numbers[0]))
    return numbers[0]

units = {
    # unit : (multiplier, category)

    # distance compared to metre
    "metre" : (1, 0),
    "kilometer" : (1000, 0),
    "centimetre" : (0.01, 0),
    "millimetre" : (0.001, 0),
    "micrometre" : (0.000001, 0),
    "mile" : (1609.344, 0),
    "foot" : (0.3048, 0),
    "feet" : (0.3048, 0),
    "inch" : (0.0254, 0),

    # mass compared to gram
    "kilogram": (1000, 1),
    "gram": (1, 1),
    "milligram": (0.001, 1),
    "microgram": (0.000001, 1),
    "tonne": (1000000, 1),
    "pound": (453.59237, 1),

    # time compared to second
    "second": (1, 2),
    "minute": (60, 2),
    "hour": (3600, 2),
    "day": (86400, 2),
    "week": (604800, 2),
    "millisecond": (0.001, 2),

    # volume compared to litre
    "litre": (1, 3),
    "millilitre": (0.001, 3),
    "centilitre": (0.01, 3),
}
search = ""
for unit in units:
    search += unit + "|"
search = search[:-1]

searchPattern = r"(\d+)\s*(" + search + ")"

def calculator(phrase):
    state.currentState = "Calculating"
    match = re.search(searchPattern, phrase)
    if match:
        amount = float(match.group(1))
        unitFrom = match.group(2)

        phrase = phrase[:match.start(2)] + phrase[match.end(2):]
        
        match = re.search(r"(" + search + ")", phrase)
        if match:
            unitTo = match.group()

            if units[unitFrom][1] == units[unitTo][1]:
                value = amount * units[unitFrom][0] / units[unitTo][0]
                value = round(value, 3)
                TTS.speak(str(value) + " " + unitTo + "s")
            else:
                TTS.speak("Can't convert from " + unitFrom + "s to " + unitTo + "s")
        else:
            TTS.speak("Unsure what unit to convert to")
    else:
        equation = phraseToEquation(phrase)
        if equation:
            calculate(equation)
        else:
            TTS.speak("Unsure what to do") # Hand to LLM
    state.currentState = "Idle"

def phraseToEquation(phrase):
    phrase = phrase.lower()
    symbols = ["+", "-", "*", "/", "(", ")", "^", "%"]
    for s in symbols:
        phrase = phrase.replace(s, f" {s} ")
    words = phrase.split()
    convertedWords = []
    for i in range(len(words)):
        convertedWords.append("")
    index = 0

    # Group numbers next to each other and "point" into one word to then give to word2number later
    currentNumber = []
    currentFirstDigit = None
    length = 0
    for i in range(len(words)):
        try:
            value = w2n.word_to_num(words[i])
            currentNumber.append(words[i])
            if not currentFirstDigit:
                currentFirstDigit = str(i)
            length += 1
        except:
            if words[i] == "point":
                currentNumber.append(words[i])
                if not currentFirstDigit:
                    currentFirstDigit = str(i)
                length += 1
            else:
                # Replace first of words used with currentNumber, clear currentNumber, set other wors used to ""
                if currentFirstDigit:
                    words[int(currentFirstDigit)] = " ".join(currentNumber)
                    for j in range(length - 1):
                        words[int(currentFirstDigit) + j + 1] = ""
                    currentFirstDigit = None
                    length = 0
                    currentNumber = []
    if currentFirstDigit:
        words[int(currentFirstDigit)] = " ".join(currentNumber)
        for j in range(length - 1):
            words[int(currentFirstDigit) + j + 1] = ""
        currentFirstDigit = None
        length = 0
        currentNumber = []

    for word in words:
        try:
            value = float(word)
            convertedWords[index] = str(value)
        except:
            try:
                value = w2n.word_to_num(word)
                convertedWords[index] = str(value)
            except:
                match word:
                    case "plus" | "add" | "+":
                        value = "+"
                    case "minus" | "subtract" | "-":
                        value = "-"
                    case "times" | "multiply" | "of" | "multiplied" | "*" | "x" | "time":
                        value = "*"
                    case "divide" | "divided" | "/":
                        value = "/"
                    case "open" | "(":
                        value = "("
                    case "close" | ")":
                        value = ")"
                    case "sin" | "sine":
                        value = "sin"
                    case "cos" | "cosine":
                        value = "cos"
                    case "tan" | "tangent":
                        value = "tan"
                    case "log" | "logarithm":
                        value = "log"
                    case "power" | "to" | "indices" | "^":
                        value = "^"
                    case "percent" | "percentage" | "%":
                        value = "%"
                    case _:
                        value = ""
                convertedWords[index] = str(value)
        index += 1
    finalWording = ""

    for word in convertedWords:
        if word != "":
            finalWording += word + " "
    return finalWording