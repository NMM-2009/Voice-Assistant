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

## Day 7
- Added basic trigonometric functions to calculator and logarithms
- Added percentages which converts the last number into a decimal so "10% of 200" would need to become "10% * 200" before being given to calculator
- Added a conversion system to convert units and more can be added by just adding them to the ```units``` dictionary
- Learnt basics of word2number on [pypi.org](https://pypi.org/project/word2number/)
- Added a function to convert sentences given to neural network into equations the calculator can tokenise and connected the calculate.py script to VoiceAssistant.py
- Fixed some bugs including it not correctly adding operators to the equations since ```.index()``` just returns the first instance of the item and a couple logic errors
- Now, VoiceAssistant.py is fully connected to Neuralnetwork.py, TTS.py, Time.py, Search.py and Calculate.py. The only functions left are the LLM and weather
- Added a State.py script which stores current info about everything that GUI.py will read from to update visuals
- Created a screen with J.A.R.V.I.S in the centre and 3 concentric rings around it

## Day 8
- Added moving arcs on the circles using ```time.monotonic()``` and added a side panel and a button to open a panel to manually enter an input
- Connected the manual enter to the rest of the scripts so that it would actually work by using threading so that the GUI.py script could still run
- Created a Theme.json file to customise the pygame_gui elements
- Made the arcs move faster when it was searching something but it didn't work and just had the arcs jump to places. It was because threads can't all get the current time so it would just make the entire movement at once. I changed the arc movement script to use dt instead and it worked
- Added ticks going around the circles and had them get longer and brighter in a wavelike pattern. The wave changes direction and moves faster when it is talking
- Made all arcs, circles and ticks turn to the warning colour when an error occurs
- Created a function to allow for notifications and called it everytime it starts searching something
- Added a section for timers that shows all current timers and what number they are after Claude showed what a UIScrollingContainer was. It also explained that each UI element had a ```.kill()``` function that needed to be called to prevent UI elements staying after their timer had been deleted or changed

## Day 9
- Added a button to the timers panel to start a new timer without having to type in an input
- Added a button to each timer entry to delete that timer
- Added a play/pause button to each timer entry and got it working after a while of debugging. The unicode pause symbol isn't supported by the font I chose so I had to spearte it into 2 line characters
- Added a button to open an alarm panel and had the panel display all active alarms and the time they would go off
- Added a delete button to the alarms
- Added a minimum window size so that GUI doesn't format weirdly when window is too small
- Created a Weather script that used open-meteo api to gt weather data from a place and date. Got it to use a geocoding api to convert a city name into coordinates then gave that to the api to get weather. It returns the lowest temperature, highest temperature and weather conditions. If the date given is the current date, it also gives the current temperature

## Day 10
- Finished off Weather.py including getting the date and time from the input phrase and using that to get data about the weather. The location extraction works by checking if it can find the location of any capitalised words in the text. If I didn't check for capitalised, it would give wrong locations due to the api just searching for the first place that includes the word given so may need to come up with a different way of doing it.
- Tried to start speech to text (STT) and used sounddevice to convert audio into a numpy vector. I tried to use faster-whisper to then convert that vector into words but my computer is too old so it wouldn't install properly and after trying for a while, I decided to leave it and to use a different library such as vosk
- Got a very small model from vosk working and connected it fully. Added a button that records when held down and immediately stops when unclicked. The model is really small so tends to mishear a lot so I made need to upgrade to a larger model. The output doesn't capitalise place names which means either I'll have to do it or find a different way to get a place name from text. Also, it records numbers as words which is fine for calculator but time will need redoing