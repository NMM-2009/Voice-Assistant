class GUIState():
    def __init__(self):
        self.talking = False
        self.currentState = "Idle"
        self.activeTimers = []
        self.activeAlarms = []

state = GUIState()