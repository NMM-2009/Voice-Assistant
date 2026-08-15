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
- Made VoiceAssistant.py and got Claude to generate some sentences which the file converted into training data for the neural network
- VoiceAssistant.py can now figure out intent if it is one of 4 functions (weather, time, calculate or search) although it struggles differentiating between weather and search sometimes because words are similar
- Fixed the confusion in the neural network by manually adding that scenario to the training data and more words to the vocabulary dictionary
- Tested out an online text to speech (TTS) module with help from [pypi.org](https://pypi.org/project/edge-tts/) and [videosdk.live](https://videosdk.live/developer-hub/ai/edge-tts)
- Used pygame-ce to play back the audio files and got it to speak from the VoiceAssistance script
- It reuses the same audio file each time so doesn't make a load of files

## Day 3
- Rewrote training data code to make it generate data based on sentences instead of hardcoding it with help from [w3 schools](https://www.w3schools.com/python/default.asp)
- Moved all training data code to be in NeuralNetwork.py
- Created Search.py to get a summary from [Wikipedia](https://www.wikipedia.org/) but had issues with permission and got 403 errors
- Changed headers to the Github repository and it worked
- Wikipedia searching worked but it would occasionally get mixed up and give unrelated articles e.g. giving information on Roman Church when asked about Roman Empire. Can probably be fixed by filtering out words since it struggles when given a sentence instead of just a topic name

## Day 4
- Separated out search and explain functionality in neural network and trained it on new data and have explain give the input to gemini
- Experimented on using DuckDuckGo API to get a quick overview for searches but it wasn't working due to it defaulting my requests to testing
- Tried out other search engine APIs but they al had issues e.g. limits and costs
- Decided to instead give the input to wikipedia and, if it was unsure of the response, give it to gemini
- Filtered out filler words to have wikipedia give better responses
- Google has age restrictions on google ai studio so can't use gemini and other models have the same so I'll leave the ai and explain sections for now
- The search function still has errors when the actual wikipedia page has strange formatting since it only gets the first paragraph from the api so, if there is an enter, it will cut short
- Learnt some html and css from Claude and [w3 schools](https://www.w3schools.com/html/default.asp)
- Got a basic design working and got a simple animation to play

## Day 5 
- Decided to restructure the searching functions once again and instead of a separate search and explain, feed it straight to a llm and tell the llm that it has access to a search tool
- Got claude to explain what a tokeniser is and how they work so I can use one for the calculate function
- Claude explained how enums work and used them to make a Token class to store what kind of token it is (the enum) and it's value
- Created the tokeniser but it repeated the first number given and never gave the last number
- I was missing a + 1 somewhere and it missed the last number since i only added the numbers when it came across a space but there is no space after the last number so it wasn't being stored anywhere
- Realised I forgot about negative numbers so I added that
- Added tokens for brackets
- Had many issues trying to combine numbers and operators back into 1 list in the right order so rewrote it to keep everything in one list and instead of adding numbers when it came across a space, it does so whenever it comes across as operator
- Had issues distinguishing between minus and a negative number in the new way but fixed by tracking if the previous token was a number or right bracket
- Had Claude explain both the shunting yard algorithm and small recursive descent parser and decided to use shunting yard algorithm as it seemed simpler to understand
- I went through multiple examples including with brackets until I understood how it worked then added created a function to do the same thing
- Created dictionary to turn operator token types into functions
- Created a calculate function to get the tokens and actually calculate with them
- Restructured it so only ```calculate()``` needs to be called, not ```calculate(shuntingYard(tokenise()))```
- Calculator still needs functionality for percentages, unit conversion, trig and exponents and maybe vectors but I decoded to start on time
- Researched the datetime library using [stack overflow](https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python)
- Added functions to get the current date and time and a stopwatch class that can track how much time has elapsed by subtracting current time from the time it was started
- Added a ```pause()``` and ```resume()``` function to the stopwatch class
- Added an alarm class that uses threads to stay on but allow scripts to do other things. It gives an invalid time message if duration is negative (would go to next day) and has cancel function and a function that is called when alarm goes off

## Day 6
- Retrained the neural network to just have 4 outputs since the search and explain will both be given to a llm
- Added training scenarios for the date
- Rewrote the neural network script to use a class and has it retrain itself if there is no preexisting weights and biases to load
- Wrote a word recogniser that could get the time related sentence and decide if it was alarm, stopwatch or date/time related but I couldn't figure out how to check if it wasn't sure (if multiple categories had the same value)
- Found the ```.count()``` function on [mimo.org](https://mimo.org/glossary/python/list-count)
- Basically remade the same function to check whether the time function was asking for the date or the time and then connected it to the TTS and to VoiceAssistant.py
- Completed alarm functionality and just need to create functions on what the alarms actually trigger which comes later
- Made VoiceAssistant.py ask for an input forever
- Added stopwatch functionality and completed all the time functions for now and connected them all directly to neural network using VoiceAssistant.py so now Wikipedia search, time and text to speech are all connected (calculate is still separate since I need to add a way to convert sentences into an equation)