import TTS
import Search
from NeuralNetwork import NeuralNetwork
import Time
import Calculate


def process(sentence):
    intentRecogniser = NeuralNetwork()

    count = intentRecogniser.sentenceToVector(sentence)
    answer = intentRecogniser.forwardPass(count)
    highest = 0
    for i in range(len(answer)):
        if answer[i] > highest:
            highest = answer[i]
            choice = i
    match choice:
        case 0:
            TTS.speak("Weather")
        case 1:
            Time.categorise(sentence)
        case 2:
            Calculate.calculator(sentence)
        case 3:
            summary = Search.search(sentence)
            TTS.speak(summary)