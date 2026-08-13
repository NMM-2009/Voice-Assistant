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
- Fixed the confusion in the neural network by manually adding that scenario to the training data and more words to the vocabulary dictionary
- Tested out an online text to speech (TTS) module with help from [pypi.org](https://pypi.org/project/edge-tts/) and [videosdk.live](https://videosdk.live/developer-hub/ai/edge-tts)
- Used pygame-ce to play back the audio files and got it to speak from the VoiceAssistance script
- It reuses the same audio file each time so doesn't make a load of files

## Day 3
- Rewrote training data code to make it generate data based on sentences instead of hardcoding it with help from [w3 schools](https://www.w3schools.com/python/default.asp)
- Moved all training data code to be in NeuralNetwork.py
- Created Search.py to get a summary from wikipedia but had issues with permission and got 403 errors
- Changed headers to the github repository and it worked
- Wikipedia searching worked but it would occasionally get mixed up and give unrelated articles e.g. giving information on Roman Church when asked about Roman Empire. Can probably be fixed by filtering out words since it struggles when given a sentence instead of just a topic name

## Day 4
- Separated out search and explain functionality in neural network and trained it on new data and have explain give the input to gemini
- Experimented on using DuckDuckGo API to get a quick overview for searches but it wasn't working due to it defaulting my requests to testing
- Tried out other search engine APIs but they al had issues e.g. limits and costs
- Decided to instead give the input to wikipedia and, if it was unsure of the response, give it to gemini
- Filtered out filler words to have wikipedia give better responses
- Google has age restrictions on google ai studio so can't use gemini and other models have the same so I'll leave the ai and explain sections for now
- The search function still has errors when the actual wikipedia page has strange formatting since it only gets the first paragraph from the api so, if there is an enter, it will cut short
- Learnt some html and css from claude and [w3 schools](https://www.w3schools.com/html/default.asp)
- Got a basic design working and got a simple animation to play