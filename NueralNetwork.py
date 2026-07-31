import random
import math

def setUp(size):
    inputs = size[0]
    outputs = size[1]

    # Set weights
    weights = []
    for i in range(outputs):
        row = []
        for j in range(inputs):
            row.append(random.uniform(-1, 1))
        weights.append(row)
    
    # Set biases
    biases = []
    for i in range(outputs):
        biases.append(random.uniform(-1, 1))
    
    return weights, biases

# Clamp values between 0 and 1 and all values sum to 1
def softmax(values):
    total = 0
    probabilities = []
    for i in range(len(values)):
        total += math.exp(values[i])
    for i in range(len(values)):
        probabilities.append(math.exp(values[i]) / total)
    return probabilities

# Matrix by vector multiplication
def mult(matrix, vector):
    answer = []
    for i in range(len(matrix)):
        total = 0
        for j in range(len(vector)):
            total += matrix[i][j] * vector[j]
        answer.append(total)
    return answer

def forwardPass(inputs, weights, biases):
    rawData = mult(weights, inputs)
    for i in range(len(rawData)):
        rawData[i] += biases[i]
    outputs = softmax(rawData)
    return outputs

def calculateLoss(guess, answer):
    error = []
    pos = answer.index(1)
    p_correct = guess[pos]
    if p_correct == 0:
        p_correct = 1e-15 # log(0) is undefined and softmax shouldn't output something between 0 and 1e-15 anyway
    for i in range(len(guess)):
        error.append(guess[i] - answer[i])
    return -(math.log(p_correct)), error

def adjust(weights, biases, inputs, error, learningRate):
    # Subtract learningRate * gradient to move in opposite direction (gradient descent)
    for i in range(len(weights)):
        for j in range(len(inputs)):
            weights[i][j] = weights[i][j] - learningRate * error[i] * inputs[j]
    for i in range(len(biases)):
        biases[i] = biases[i] - learningRate * error[i]
    return weights, biases


trainingData = [
    [[0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]],
    [[0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]],
    [[0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]],
    [[0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]],
    [[0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]],
    [[0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
]

weights, biases = setUp([len(trainingData[0][0]), len(trainingData[0][1])])
learningRate = 0.5

for epoch in range(1000):
    totalLoss = 0

    for number in range(len(trainingData)):
        inputs = trainingData[number][0]
        answer = trainingData[number][1]

        guess = forwardPass(inputs, weights, biases)
        loss, error = calculateLoss(guess, answer)
        weights, biases = adjust(weights, biases, inputs, error, learningRate)
        totalLoss += loss
    
    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Average loss: {totalLoss / len(trainingData)}")
