import requests
import re
import datetime
import TTS
from State import state

# Input -> break into date and time by looking at prepositions and words before/after -> geocoding (turn location into coordinates) -> get info from Open-Meteo

baseURL = "https://api.open-meteo.com/v1/forecast?"
baseGeoURL = "https://geocoding-api.open-meteo.com/v1/search?"

weatherParams = {
    "latitude" : 52.63, "longitude" : -1.13,
    "timezone" : "auto",
    "current_weather" : True,
    "daily": "temperature_2m_max,temperature_2m_min,weathercode"
}

def getCoordinates(place):

    geoParams = {
        "name" : place,
        "count" : 1
    }

    site = requests.get(baseGeoURL, params = geoParams)
    site = site.json()

    weatherParams.update({"latitude" : site["results"][0]["latitude"], "longitude" : site["results"][0]["longitude"]})

def getData(date):
    weather = requests.get(baseURL, params = weatherParams)
    weather = weather.json()

    if date in weather["daily"]["time"]:
        dayIndex = weather["daily"]["time"].index(date)
    else:
        state.currentState = "Error"
        state.justChanged = True
        TTS.speak("Can't get weather for that date")
        state.currentState = "Idle"
        state.justChanged = True
        return None

    minTemp = str(weather["daily"]["temperature_2m_min"][dayIndex]) + weather["daily_units"]["temperature_2m_min"]
    maxTemp = str(weather["daily"]["temperature_2m_max"][dayIndex]) + weather["daily_units"]["temperature_2m_max"]

    if dayIndex == 0:
        currentTemp = str(weather["current_weather"]["temperature"]) + weather["current_weather_units"]["temperature"]
        speech = (f"It's currently {currentTemp} with a minimum temperature of {minTemp} and maximum of {maxTemp} today")
    else:
        speech = (f"Predicted to have minimum temperature of {minTemp} and maximum temperature of {maxTemp}")

    weatherCondition = weather["daily"]["weathercode"][dayIndex]
    if weatherCondition == 0:
        condition = "clear skies"
    elif weatherCondition >= 1 and weatherCondition <= 3:
        condition = "partly cloudy skies"
    elif weatherCondition == 45 or weatherCondition == 48:
        condition = "fog"
    elif weatherCondition >= 51 and weatherCondition <= 57:
        condition = "a drizzle"
    elif weatherCondition >= 61 and weatherCondition <= 67:
        condition = "rain"
    elif weatherCondition >= 71 and weatherCondition <= 77:
        condition = "snow"
    elif weatherCondition >= 80 and weatherCondition <= 82:
        condition = "rain showers"
    elif weatherCondition >= 85 and weatherCondition <= 86:
        condition = "snow showers"
    elif weatherCondition == 95:
        condition = "thunderstorms"
    elif weatherCondition >= 96 and weatherCondition <= 99:
        condition = "thunderstorms with hail"
    else:
        condition = ""
    
    if condition != "":
        speech = speech + ". Expect " + condition
    
    state.currentState = "Idle"
    state.justChanged = True
    TTS.speak(speech)

def getCity(phrase):
    found = False
    words = phrase.split()
    for position, word in enumerate(words):
        if not found:
            for i in range(len(words) - 1, position - 1, -1):
                checkPhrase = " ".join(words[position : i + 1])
                if any(char.isupper() for char in checkPhrase):
                    try:
                        getCoordinates(checkPhrase)
                        found = True
                        break
                    except:
                        continue
                else:
                    continue
        else:
            break
    if not found:
        getCoordinates("Leicester")

def getDate(phrase):
    phrase = phrase.lower()
    words = phrase.split()
    offset = ""

    dayOffset = {
        "today" : 0,
        "tomorrow" : 1,
    }

    for word in words:
        if word in dayOffset:
            offset = dayOffset[word]
            break

    match = re.search(r"(\d+)(\s*day)", phrase)
    if match:
        offset = int(match.group(1))

    now = datetime.datetime.now()

    days = {
        "monday" : 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    for word in words:
        if word in days:
            target = days[word]
            current = now.weekday()
            offset = (target - current) % 7

    if offset != "":
        now = now + datetime.timedelta(days = offset)
        return now.strftime("%Y-%m-%d")

    match = re.search(r"(\d{1,2})\s*(?:st|nd|rd|th)", phrase)
    if match:
        day = int(match.group(1))
        date = now.replace(day = day)
        return date.strftime("%Y-%m-%d")
    
    return now.strftime("%Y-%m-%d")

def getWeather(phrase):
    state.currentState = "Thinking"
    state.justChanged = True
    getCity(phrase)
    getData(getDate(phrase))