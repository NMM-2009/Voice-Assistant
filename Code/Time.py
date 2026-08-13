# Needs to take input from neural network and do basic keyword positioning logic and keyword search to get stopwatch, alarm, current time and operand (time)

import datetime
import time
import threading

def currentTime():
    now = datetime.datetime.now()
    return str(now.hour) + ":" + str(now.minute)

def currentPreciseTime():
    now = datetime.datetime.now()
    return now.time()

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