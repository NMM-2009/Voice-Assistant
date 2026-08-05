import NeuralNetwork as nn
import ast
import TTS

file = open("NeuralNetworkSetting.txt", "r")
weights = ast.literal_eval(file.readline())
biases = ast.literal_eval(file.readline())
file.close()

sentence = input("Enter sentence: ")
count = nn.sentenceToVector(sentence)
answer = nn.forwardPass(count, weights, biases)
highest = 0
for i in range(len(answer)):
    if answer[i] > highest:
        highest = answer[i]
        choice = i
match choice:
    case 0:
        TTS.speak("Weather")
    case 1:
        TTS.speak("Time")
    case 2:
        TTS.speak("Calculate")
    case 3:
        TTS.speak("Search")