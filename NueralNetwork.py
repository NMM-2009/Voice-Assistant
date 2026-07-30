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
    return(outputs)
