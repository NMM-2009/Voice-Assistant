import NeuralNetwork as nn
import ast

file = open("NeuralNetworkSetting.txt", "r")
weights = ast.literal_eval(file.readline())
biases = ast.literal_eval(file.readline())
file.close()

vocabulary = {
    "what": 0, "whats": 1, "is": 2, "the": 3, "today": 4, "like": 5,
    "weather": 6, "temperature": 7, "forecast": 8, "rain": 9, "sunny": 10,
    "cold": 11, "hot": 12, "outside": 13, "degrees": 14, "in": 15,

    "set": 16, "timer": 17, "alarm": 18, "for": 19, "minutes": 20,
    "seconds": 21, "hours": 22, "start": 23, "countdown": 24, "remind": 25,
    "me": 26, "cancel": 27, "stop": 28,

    "calculate": 29, "plus": 30, "minus": 31, "times": 32, "divided": 33,
    "by": 34, "percent": 35, "of": 36, "convert": 37, "to": 38, "sum": 39,
    "add": 40, "subtract": 41, "multiply": 42, "divide": 43, "equals": 44,

    "who": 45, "search": 46, "look": 47, "up": 48, "find": 49, "tell": 50,
    "about": 51, "information": 52, "define": 53, "meaning": 54,
    "explain": 55, "summarize": 56, "wikipedia": 57, "why": 58, "how": 59,
    "when": 60, "where": 61
}


#sentences = [
#    "whats the weather like today", [1, 0, 0, 0],
#    "is it going to rain", [1, 0, 0, 0],
#    "what is the temperature outside", [1, 0, 0, 0],
#    "will it be sunny tomorrow", [1, 0, 0, 0],
#    "how cold is it today", [1, 0, 0, 0],
#
#    "set a timer for 10 minutes", [0, 1, 0, 0],
#    "set an alarm for 6 hours", [0, 1, 0, 0],
#    "remind me in 5 minutes", [0, 1, 0, 0],
#    "start a countdown for 30 seconds", [0, 1, 0, 0],
#    "cancel the timer", [0, 1, 0, 0],
#
#    "calculate 15 times 8", [0, 0, 1, 0],
#    "whats 20 percent of 80", [0, 0, 1, 0],
#    "convert 5 miles to kilometers", [0, 0, 1, 0],
#    "what is 100 divided by 4", [0, 0, 1, 0],
#    "add 12 and 7", [0, 0, 1, 0],
#
#    "who is the president", [0, 0, 0, 1],
#    "search for the tallest mountain", [0, 0, 0, 1],
#    "tell me about the solar system", [0, 0, 0, 1],
#    "define photosynthesis", [0, 0, 0, 1],
#    "how does a car engine work", [0, 0, 0, 1],
#]
#inputs = []
#answers = []
#for j in range(0, len(sentences), 2):
#    count = [0] * len(vocabulary)
#    sentence = sentences[j]
#    sentence = sentence.lower()
#    words = sentence.split()
#    for i in range(len(words)):
#        if words[i] in vocabulary:
#            count[vocabulary[words[i]]] += 1
#    inputs.append(count)
#    answers.append(sentences[j + 1])

sentence = input("Enter sentence: ")
sentence = sentence.lower()
words = sentence.split()
count = [0] * len(vocabulary)
for i in range(len(words)):
    if words[i] in vocabulary:
        count[vocabulary[words[i]]] += 1
answer = nn.forwardPass(count, weights, biases)
highest = 0
for i in range(len(answer)):
    if answer[i] > highest:
        highest = answer[i]
        choice = i
match choice:
    case 0:
        print("Weather")
    case 1:
        print("Time")
    case 2:
        print("Calculate")
    case 3:
        print("Search")