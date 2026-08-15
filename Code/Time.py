# Needs to take input from neural network and do basic keyword positioning logic and keyword search to get stopwatch, alarm, current time and operand (time)

import datetime
import time
import threading
import TTS
import re

def currentTime():
    now = datetime.datetime.now()
    return str(now.hour) + ":" + str(now.minute)

def preciseTime():
    now = datetime.datetime.now()
    return str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

def currentDate():
    now = datetime.datetime.now()
    return  now.date().strftime("%A %d %B %Y")

class Stopwatch():
    def __init__(self):
        self.start = time.monotonic()
        self.offset = 0
        self.paused = False
        self.pauseStart = 0
    
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
        self.startTime = preciseTime()
        self.stopTime = stopTime
        self.valid = True
        # stopTime given as HH:MM
        self.goalHours, self.goalMinutes, self.goalSeconds = stopTime.split(":")
        self.hours, self.minutes, self.seconds = preciseTime().split(":")

        self.goalHours = int(self.goalHours)
        self.goalMinutes = int(self.goalMinutes)
        self.goalSeconds = int(self.goalSeconds)

        self.hours = int(self.hours)
        self.minutes = int(self.minutes)
        self.seconds = int(self.seconds)

        self.hours = self.goalHours - self.hours
        self.minutes = self.goalMinutes - self.minutes
        self.seconds = self.goalSeconds - self.seconds

        self.seconds += self.minutes * 60
        self.seconds += self.hours * 3600
        self.duration = self.seconds

        if self.duration < 0:
            self.valid = False

        if self.valid:
            self.thread = threading.Timer(self.duration, self.alarm)
            self.thread.start()
        else:
            TTS.speak("Invalid time")

    def alarm(self):
        delete(self)
        TTS.speak("Alarm up")

    def cancel(self):
        self.thread.cancel()

def delete(alarm):
    if alarm in alarms:
        alarms.remove(alarm)
    else:
        TTS.speak("That timer doesn't exist")

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
    match categories.index(highest):
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

    match categories.index(highest):
        case 0:
            TTS.speak("The time is " + currentTime())
        case 1:
            TTS.speak("It's " + currentDate())

alarmFunctionWords = {
    "set" : (2, 0),
    "remind" : (2, 0),
    "start" : (2, 0),

    "cancel" : (2, 1),
    "stop" : (2, 1),
    "undo" : (2, 1),
    "delete" : (2, 1),
    "end" : (2, 1),
}

alarms = []

def getAlarmFunction(phrase):
    words = phrase.split()
    categories = [0, 0]

    for word in words:
        try:
            weight, category = alarmFunctionWords[word]
            categories[category] += 1 * weight
        except:
            pass

    highest = 0
    for i in categories:
       if i > highest:
           highest = i

    if categories.count(highest) > 1:
        TTS.speak("Unsure of your request")

    alarmTime = getAlarmTime(phrase)

    match categories.index(highest):
        case 0:
            # Check if time given
            if re.search(r"\d{1,2}:\d{2}:\d{2}", alarmTime):
                endTime = alarmTime
                alarms.append(Alarm(endTime))
                TTS.speak("Alarm started")

            # Check if duration given in seconds
            elif re.search(r"\d+", alarmTime):
                hours, minutes, seconds = preciseTime().split(":")
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)

                seconds += int(alarmTime)

                while seconds >= 60:
                    minutes += 1
                    seconds -= 60

                while minutes >= 60:
                    hours += 1
                    minutes -= 60

                if hours >= 24:
                    hours -= 24

                endTime = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                alarms.append(Alarm(endTime))
                TTS.speak("Alarm started")
            else:
                TTS.speak("No valid time")
        case 1:
            # Check if time given
            if re.search(r"\d{1,2}:\d{2}:\d{2}", alarmTime):
                alarmID = alarmTime
                for alarm in alarms:
                    if alarm.stopTime == alarmID:
                        alarm.cancel()
                        delete(alarm)
                        TTS.speak("Alarm deleted")
            # Check if duration given
            elif re.search(r"\d+", alarmTime):
                # "Stop the 30 minute alarm" checks for any alarms that were 30 mins long
                for alarm in alarms:
                    if str(int(alarm.duration)) == alarmTime:
                        alarm.cancel()
                        delete(alarm)
                        TTS.speak("Alarm deleted")
            else:
                TTS.speak("No valid time")

def getAlarmTime(phrase):
    # Check for HH am/pm or HH:MM am/pm or HH:MM:SS am/pm
    match = re.search(r"(\d{1,2})(:\d{2})?(:\d{2})?\s*(am|pm)", phrase)
    if match:
        hour = match.group(1)
        # Turn into 24 hour clock
        if match.group(4) == "pm":
            hour = str(int(hour) + 12)
        # Set midnight time to start with 0
        elif hour == "12":
            hour = "0"
        
        # Add minutes
        if match.group(2):
            minutes = match.group(2)
        else:
            minutes = ":00" 

        # Add seconds
        if match.group(3):
            seconds = match.group(3)
        else:
            seconds = ":00"
        return hour + minutes + seconds
    
    # Check for HH:MM or H:MM or with :SS
    match = re.search(r"(\d{1,2}:\d{2})(:\d{2})?", phrase)
    if match:
        if match.group(2):
            return match.group()
        else:
            return match.group() + ":00"
    
    # Search for the duration and convert to seconds
    # Return number of seconds
    match = re.search(r"(\d+)\s*(second|seconds|minute|minutes|hour|hours)", phrase)
    if match:
        unit = match.group(2)
        if unit == "second" or unit == "seconds":
            return str(match.group(1))
        elif unit == "minute" or unit == "minutes":
            return str(int(match.group(1)) * 60)
        elif unit == "hour" or unit == "hours":
            return str(int(match.group(1)) * 3600)
        else:
            TTS.speak("Couldn't recognise unit")
            return "Error"
    return "Error"

stopwatchFunctionWords = {
    "start" : (2, 0),
    "begin" : (2, 0),
    "set" : (2, 0),

    "end" : (2, 1),
    "stop" : (1, 1),
    "delete" : (2, 1),
    "cancel" : (2, 1),

    "pause" : (2, 2),
    "break" : (2, 2),

    "continue" : (2, 3),
    "resume" : (2, 3),
    "unpause" : (2, 3),

    "update" : (2, 4),
    "what" : (1, 4),
    "whats" : (1, 4),
    "at" : (1, 4),
    "current" : (2, 4),
}

stopwatches = []

def getStopwatchFunction(phrase):
    words = phrase.split()
    categories = [0, 0, 0, 0, 0]

    for word in words:
        try:
            weight, category = stopwatchFunctionWords[word]
            categories[category] += 1 * weight
        except:
            pass

    highest = 0
    for i in categories:
       if i > highest:
           highest = i

    if categories.count(highest) > 1:
        TTS.speak("Unsure of your request")
        return 0

    match categories.index(highest):
        case 0:
            stopwatches.append(Stopwatch())
            TTS.speak("Started a timer")
        case 1:
            index = whichStopwatch(phrase)
            if index:
                stopwatches.pop(int(index))
                TTS.speak("Deleted the timer")
        case 2:
            index = whichStopwatch(phrase)
            if index:
                if not stopwatches[int(index)].paused:
                    stopwatches[int(index)].pause()
                    TTS.speak("Paused the timer")
                else:
                    TTS.speak("Timer is already paused")
        case 3:
            index = whichStopwatch(phrase)
            if index:
                if stopwatches[int(index)].paused:
                    stopwatches[int(index)].resume()
                    TTS.speak("Resumed the timer")
                else:
                    TTS.speak("Timer isn't paused")
        case 4:
            index = whichStopwatch(phrase)
            if index:
                TTS.speak("The timer is at " + str(stopwatches[int(index)].update()) + " seconds")

def whichStopwatch(phrase):
    match = re.search(r"\d+", phrase) # Assume any number is the stopwatch index
    if match:
        return match.group()
    else:
        TTS.speak("Unsure which timer")
        return None