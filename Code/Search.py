import requests
from State import state

def search(question):
    state.currentState = "Searching"
    fillerWords = [
        "who", "what", "when", "where", "why", "how", "is", "are", "was",
        "were", "do", "does", "did", "can", "could", "will", "would", 
        "should", "the", "a", "an", "of", "to", "for", "in", "on", "at",
        "me", "my", "i", "you", "your", "please", "tell", "about",
        "whats", "hows", "wheres", "whens"
    ]
    
    words = question.split()
    keyWords = ""
    for word in words:
        if word not in fillerWords:
            keyWords = keyWords + " " + word
    topic = keyWords

    url = "https://en.wikipedia.org/w/rest.php/v1/search/page"
    params = {"q" : topic, "limit" : 1}
    headers = { "User-Agent" : "Voice-Assistant/0.1 (https://github.com/NMM-2009/Natural-Language-UI)"}
    temp = requests.get(url, params = params, headers = headers)

    data = temp.json()
    title = data["pages"][0]['title']

    temp = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}", headers = headers)
    page = temp.json()
    
    summary = page["extract"]
    state.currentState = "Idle"
    return summary
