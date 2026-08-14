import random
import math
import ast

class NeuralNetwork():
    def __init__(self):
        self.buildVocabulary()
        try:
            file = open("NeuralNetworkSetting.txt", "r")
            self.weights = ast.literal_eval(file.readline())
            self.biases = ast.literal_eval(file.readline())
            file.close()
        except:
            self.train()
    
    def setUp(self, size):
        inputs = size[0]
        outputs = size[1]

        # Set weights
        self.weights = []
        for i in range(outputs):
            self.row = []
            for j in range(inputs):
                self.row.append(random.uniform(-1, 1))
            self.weights.append(self.row)

        # Set biases
        self.biases = []
        for i in range(outputs):
            self.biases.append(random.uniform(-1, 1))

    # Clamp values between 0 and 1 and all values sum to 1
    def softmax(self, values):
        total = 0
        probabilities = []
        for i in range(len(values)):
            total += math.exp(values[i])
        for i in range(len(values)):
            probabilities.append(math.exp(values[i]) / total)
        return probabilities

    # Matrix by vector multiplication
    def mult(self, matrix, vector):
        answer = []
        for i in range(len(matrix)):
            total = 0
            for j in range(len(vector)):
                total += matrix[i][j] * vector[j]
            answer.append(total)
        return answer

    def forwardPass(self, inputs):
        rawData = self.mult(self.weights, inputs)
        for i in range(len(rawData)):
            rawData[i] += self.biases[i]
        outputs = self.softmax(rawData)
        return outputs

    def calculateLoss(self, guess, answer):
        error = []
        pos = answer.index(1)
        p_correct = guess[pos]
        if p_correct == 0:
            p_correct = 1e-15 # log(0) is undefined and softmax shouldn't output something between 0 and 1e-15 anyway
        for i in range(len(guess)):
            error.append(guess[i] - answer[i])
        return -(math.log(p_correct)), error

    def adjust(self, inputs, error, learningRate):
        # Subtract learningRate * gradient to move in opposite direction (gradient descent)
        for i in range(len(self.weights)):
            for j in range(len(inputs)):
                self.weights[i][j] = self.weights[i][j] - learningRate * error[i] * inputs[j]
        for i in range(len(self.biases)):
            self.biases[i] = self.biases[i] - learningRate * error[i]

    def sentenceToVector(self, sentence):
        sentence = sentence.lower()
        words = sentence.split()
        count = [0] * len(self.trainingWords)
        for i in range(len(words)):
            if words[i] in self.trainingWords:
                count[self.trainingWords[words[i]]] += 1
        return count

    def getTrainingData(self):
        self.trainingData = []
        for i in range(0, len(self.sentences), 2):
            vector = self.sentenceToVector(self.sentences[i])
            self.trainingData.append([vector, self.sentences[i + 1]])

    def buildVocabulary(self):
        # Answer format
        # [weather, time, calculate, llm]
        self.sentences = [
            "whats the weather like today", [1, 0, 0, 0],
            "is it going to rain", [1, 0, 0, 0],
            "what is the temperature outside", [1, 0, 0, 0],
            "will it be sunny tomorrow", [1, 0, 0, 0],
            "how cold is it today", [1, 0, 0, 0],
            "is it hot outside", [1, 0, 0, 0],
            "whats the forecast for tomorrow", [1, 0, 0, 0],
            "how many degrees is it right now", [1, 0, 0, 0],
            "is it going to snow this week", [1, 0, 0, 0],
            "what is the weather forecast", [1, 0, 0, 0],
            "will it rain later", [1, 0, 0, 0],
            "how windy is it outside", [1, 0, 0, 0],
            "is it cloudy today", [1, 0, 0, 0],
            "whats the temperature like outside", [1, 0, 0, 0],
            "will it be cold tonight", [1, 0, 0, 0],
            "do i need a jacket today", [1, 0, 0, 0],
            "should i bring an umbrella", [1, 0, 0, 0],
            "will i need sunglasses today", [1, 0, 0, 0],
            "is it a good day to hang washing outside", [1, 0, 0, 0],
            "do i need a coat this morning", [1, 0, 0, 0],

            "set a timer for 10 minutes", [0, 1, 0, 0],
            "set an alarm for 6 hours", [0, 1, 0, 0],
            "remind me in 5 minutes", [0, 1, 0, 0],
            "start a countdown for 30 seconds", [0, 1, 0, 0],
            "cancel the timer", [0, 1, 0, 0],
            "what is the time", [0, 1, 0, 0],
            "set a timer for 2 hours", [0, 1, 0, 0],
            "stop the alarm", [0, 1, 0, 0],
            "remind me in 20 seconds", [0, 1, 0, 0],
            "set an alarm for 7am", [0, 1, 0, 0],
            "start a timer for 45 minutes", [0, 1, 0, 0],
            "cancel the alarm", [0, 1, 0, 0],
            "set a countdown for 1 hour", [0, 1, 0, 0],
            "remind me to stop in 10 minutes", [0, 1, 0, 0],
            "stop the timer", [0, 1, 0, 0],
            "whats the date today", [0, 1, 0, 0],
            "what is the date", [0, 1, 0, 0],
            "what day is it", [0, 1, 0, 0],
            "what day of the week is it", [0, 1, 0, 0],
            "what month is it", [0, 1, 0, 0],
            "what year is it", [0, 1, 0, 0],

            "calculate 15 times 8", [0, 0, 1, 0],
            "whats 20 percent of 80", [0, 0, 1, 0],
            "convert 5 miles to kilometers", [0, 0, 1, 0],
            "what is 100 divided by 4", [0, 0, 1, 0],
            "add 12 and 7", [0, 0, 1, 0],
            "subtract 9 from 20", [0, 0, 1, 0],
            "multiply 6 by 7", [0, 0, 1, 0],
            "whats the sum of 4 and 9", [0, 0, 1, 0],
            "calculate 50 minus 12", [0, 0, 1, 0],
            "convert 10 kilometers to miles", [0, 0, 1, 0],
            "what is 9 plus 16", [0, 0, 1, 0],
            "divide 100 by 5", [0, 0, 1, 0],
            "whats 15 percent of 200", [0, 0, 1, 0],
            "calculate 30 divided by 6", [0, 0, 1, 0],
            "what does 8 times 8 equal", [0, 0, 1, 0],

            "who is the president", [0, 0, 0, 1],
            "search for the tallest mountain", [0, 0, 0, 1],
            "tell me about the solar system", [0, 0, 0, 1],
            "define photosynthesis", [0, 0, 0, 1],
            "what is the largest planet in our solar system", [0, 0, 0, 1],
            "who invented the telephone", [0, 0, 0, 1],
            "look up the population of london", [0, 0, 0, 1],
            "find information about black holes", [0, 0, 0, 1],
            "when was the eiffel tower built", [0, 0, 0, 1],
            "where is the great barrier reef", [0, 0, 0, 1],
            "according to wikipedia what is gravity", [0, 0, 0, 1],
            "what did albert einstein discover", [0, 0, 0, 1],
            "how tall is the eiffel tower", [0, 0, 0, 1],
            "how far is the moon from earth", [0, 0, 0, 1],
            "how old is stonehenge", [0, 0, 0, 1],
            "how many countries are there in the world", [0, 0, 0, 1],
            "how big is the pacific ocean", [0, 0, 0, 1],

            "what is the weather", [1, 0, 0, 0],
            "what is the temperature right now", [1, 0, 0, 0],

            "what is the time right now", [0, 1, 0, 0],
            "what is the countdown at", [0, 1, 0, 0],

            "what is 9 plus 10", [0, 0, 1, 0],
            "what is the sum of 3 and 4", [0, 0, 1, 0],

            "what is the oldest book in the world", [0, 0, 0, 1],
            "what is the tallest building in the world", [0, 0, 0, 1],
            "what is a black hole", [0, 0, 0, 1],
            "what is the capital of france", [0, 0, 0, 1],
            "what is the fastest animal on earth", [0, 0, 0, 1],
            "how many moons does jupiter have", [0, 0, 0, 1],
            "is the sun bigger than the earth", [0, 0, 0, 1],

            "explain how photosynthesis works", [0, 0, 0, 1],
            "how does a car engine work", [0, 0, 0, 1],
            "why is the sky blue", [0, 0, 0, 1],
            "how do airplanes fly", [0, 0, 0, 1],
            "how long does it take to boil an egg", [0, 0, 0, 1],
            "is it possible to divide by zero", [0, 0, 0, 1],
            "why does ice float on water", [0, 0, 0, 1],
            "why do we dream", [0, 0, 0, 1],
            "how does wifi actually work", [0, 0, 0, 1],
            "why is the ocean salty", [0, 0, 0, 1],
            "how does a computer store memory", [0, 0, 0, 1],
            "explain how vaccines work", [0, 0, 0, 1],
            "why do magnets attract each other", [0, 0, 0, 1],
            "how does encryption keep data safe", [0, 0, 0, 1],
            "why does metal feel colder than wood", [0, 0, 0, 1],
            "explain how a neural network learns", [0, 0, 0, 1],
            "why is my code throwing an error", [0, 0, 0, 1],
            "explain why my servo keeps jittering", [0, 0, 0, 1],
            "why isn't my sensor giving accurate readings", [0, 0, 0, 1],
            "how do i fix a syntax error", [0, 0, 0, 1],
            "why does my loop never end", [0, 0, 0, 1],
            "explain the difference between a list and a dictionary", [0, 0, 0, 1],
            "why is my arduino not connecting", [0, 0, 0, 1],
        ]

        words = set()
        for i in range(0, len(self.sentences), 2):
            temp = self.sentences[i]
            temp = temp.lower()
            temp = temp.split()
            for word in temp:
                words.add(word)

        temp = list(words)
        temp.sort()
        self.trainingWords = {word: index for index, word in enumerate(temp)}

    def train(self):
        self.getTrainingData()
        self.setUp([len(self.trainingData[0][0]), len(self.trainingData[0][1])])
        learningRate = 0.5

        for epoch in range(2000):
            for number in range(len(self.trainingData)):
                inputs = self.trainingData[number][0]
                answer = self.trainingData[number][1]
                guess = self.forwardPass(inputs)
                loss, error = self.calculateLoss(guess, answer)
                self.adjust(inputs, error, learningRate)

        settingsFile = open("NeuralNetworkSetting.txt", "w")
        settingsFile.write(str(self.weights))
        settingsFile.write("\n")
        settingsFile.write(str(self.biases))
        settingsFile.write("\n")
        settingsFile.close()

        print("Done training")