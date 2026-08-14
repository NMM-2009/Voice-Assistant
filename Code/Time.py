# Needs to take input from neural network and do basic keyword positioning logic and keyword search to get stopwatch, alarm, current time and operand (time)

import datetime
import time
import threading
import TTS

def currentTime():
    now = datetime.datetime.now()
    return str(now.hour) + ":" + str(now.minute)

def currentDate():
    now = datetime.datetime.now()
    return  now.date().strftime("%A %d %B %Y")

class StopWatch():
    def __init__(self):
        self.start = time.monotonic()
        self.offset = 0
        self.paused = False
    
    def update(self):
        if self.paused:
            return int(self.pauseStart - self.start - self.offset)
        else:
            return int(time.monotonic() - self.start - self.offset)
    
    def pause(self):
        self.pauseStart = time.monotonic()
        self.paused = True

    def resume(self):
        self.offset += time.monotonic() - self.pauseStart
        self.paused = False

class Alarm():
    def __init__(self, stopTime):
        self.valid = True
        # stopTime given as HH:MM
        self.goalHours, self.goalMinutes = stopTime.split(":")
        self.hours, self.minutes = currentTime().split(":")

        self.goalHours = int(self.goalHours)
        self.goalMinutes = int(self.goalMinutes)
        self.hours = int(self.hours)
        self.minutes = int(self.minutes)

        self.hours = self.goalHours - self.hours
        self.minutes = self.goalMinutes - self.minutes

        self.minutes += self.hours * 60
        self.duration = self.minutes * 60

        if self.duration < 0:
            self.valid = False

        if self.valid:
            self.thread = threading.Timer(self.duration, self.alarm)
            self.thread.start()
        else:
            print("Invalid time")

    def alarm(self):
        print("Alarm up")

    def cancel(self):
        self.thread.cancel()

categoryWords = {
    # word : (weight, category)

    # Words to call alarm
    "alarm" : (2, 0),
    "wake" : (2, 0),
    "wakeup" : (2, 0),
    "remind" : (2, 0),

    # Words to call stopwatch
    "timer" : (2, 1),
    "stopwatch" : (2, 1),

    # Words to get date/time
    "date" : (2, 2),
    "time" : (1, 2),
    "day" : (2, 2),
    "month" : (2, 2),
    "year" : (2, 2),
    "clock" : (1, 2),
}

def categorise(phrase):
    phrase = phrase.lower()
    words = phrase.split()
    categories = [0, 0, 0]

    for word in words:
        try:
            weight, category = categoryWords[word]
            categories[category] += 1 * weight
        except:
            pass

    highest = 0
    for i in categories:
        if i > highest:
            highest = i

    if categories.count(highest) > 1:
        print("Unsure") # Will connect to the LLM
    match category:
        case 0:
            getAlarmFunction(phrase)
        case 1:
            getStopwatchFunction(phrase)
        case 2:
            getTimeFunction(phrase)


timeFunctionWords = {
    "time" : (2, 0),
    "clock" : (1, 0),

    "date" : (2, 1),
    "day" : (2, 1),
    "month" : (2, 1),
    "year" : (2, 1),
    "week" : (2, 1),

}

def getTimeFunction(phrase):
    words = phrase.split()
    categories = [0, 0]

    for word in words:
        try:
            weight, category = timeFunctionWords[word]
            categories[category] += 1 * weight
        except:
            pass

    highest = 0
    for i in categories:
       if i > highest:
           highest = i

    if categories.count(highest) > 1:
        print("Unsure") # Will connect to the LLM

    match category:
        case 0:
            TTS.speak("The time is " + currentTime())
        case 1:
            TTS.speak("It's " + currentDate())

def getAlarmFunction(phrase):
    pass

def getStopwatchFunction(phrase):
    pass