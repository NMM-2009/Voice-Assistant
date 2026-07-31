# Build Notes

## Day 1
- Learnt about neural networks and how they work from [Sebastian Lague](https://www.youtube.com/watch?v=hfMk-kjRv4c) although he used C# and I plan on using python
- Created functions for neural network to fully compute a forward pass using matrix by vector multiplication
- Initialises using random weights and biases
- Will be trained and used to recognise what function to execute based on a spoken input (intent recogniser)
- Uses a softmax function instead of sigmoid function like Sebastian Lague uses so that the outputs given are probabilities
- Currently doesn't allow for hidden layers

## Day 2
- Added function for calculating loss
- Claude explained gradient descent and how to adjust the weights and biases
- Added functions for training and tested it on made up data and got loss down from 2.9989 to 0.00029 after 1000 iterations
- Learnt about epochs and added a way to train with multiple test inputs and answers
- Got neural network to save it's weights and biases into a text file with help from [w3 schools](https://www.w3schools.com/python/python_file_open.asp)
- Made VoiceAssistant.py and got claude to generate some sentences which the file converted into training data for the neural network
- VoiceAssistant.py can now figure out intent if it is one of 4 functions (weather, time, calculate or search) although it struggles differentiating between weather and search sometimes because words are similar
- Tested out an online text to speech (TTS) module with help from [pypi.org](https://pypi.org/project/edge-tts/) and [videosdk.live](https://videosdk.live/developer-hub/ai/edge-tts)
- Used pygame-ce to play back the audio files and got it to speak from the VoiceAssistance script
- It reuses the same audio file each time so doesn't make a load of files