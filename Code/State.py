class GUIState():
    def __init__(self):
        self.talking = False
        self.currentState = "Idle"
        self.justChanged = False
        self.activeTimers = []
        self.activeAlarms = []
        self.listening = False

state = GUIState()