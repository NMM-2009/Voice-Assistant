import math
import threading
import pygame
import pygame_gui as gui
from State import state
import VoiceAssistant
import Calculate

# Settings variables (not including colours)
holdTime = 1

dt = 0

width, height = 1500, 1000

backgroundColour = (20, 20, 30) #14141E
primaryColour = (0, 200, 255) #00C8FF
secondaryColour = (10, 80, 130) #0A5082
highlightColour = (120, 240, 255) #78F0FF
textColour = (200, 235, 255) #C8EBFF
warningColour = (255, 170, 60) #FFAA3C
secondaryWarningColour = (153, 102, 36) #994823

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("J.A.R.V.I.S")
manager = gui.UIManager((width, height), "Theme.json")

class Arc():
    def __init__(self, startPosition, speed, length, ring):
        self.startPos = startPosition # In radians
        self.speed = speed # Positive for anticlockwise, negative for clockwise
        self.length = length # In radians
        self.ring = ring

        self.update()

    def update(self):
        global dt
        if self.ring == 1:
            rect = (width // 2 - height // 6, height // 3, height // 3, height // 3)
        elif self.ring == 2:
            rect = (width // 2 - height // 4, height // 4, height // 2, height // 2)
        else:
            rect = (width // 2 - height // 3, height // 2 - height // 3, 2 * height // 3, 2 * height // 3)

        if state.currentState == "Searching":
            mult = -0.5
        else:
            mult = 0.05

        self.startPos += self.speed * dt * mult

        if state.currentState == "Error":
            self.colour = warningColour
        else:
            self.colour = primaryColour

        pygame.draw.arc(screen, self.colour, pygame.Rect(rect), self.startPos, self.startPos + self.length, 4)

class Tick():
    def __init__(self, angle):
        self.angle = angle # In radians
        self.length = 10
        self.colour = (10, 80, 130)

    def update(self):
        raw = abs(self.angle - wavePos)
        distance = min(raw, 2 * math.pi - raw)
        self.intensity = max(0, math.cos(distance))

        self.length = 10 + self.intensity * 10

        if state.currentState == "Error":
            self.colour = tuple(int(a + (b - a) * self.intensity) for a, b in zip(secondaryWarningColour, warningColour))
        elif state.currentState == "Calculating":
            self.colour = tuple(int(a + (b - a) * self.intensity) for a, b in zip(secondaryColour, warningColour))
        else:
            self.colour = tuple(int(a + (b - a) * self.intensity) for a, b in zip(secondaryColour, primaryColour))

        self.sx, self.sy = math.cos(self.angle) * 5 * height / 14, math.sin(self.angle) * 5 * height / 14
        self.start = (width / 2 + self.sx, height / 2 + self.sy)
        self.ex, self.ey = math.cos(self.angle) * self.length + self.sx, math.sin(self.angle) * self.length + self.sy
        self.end = (width / 2 + self.ex, height / 2 + self.ey)

        pygame.draw.line(screen, self.colour, self.start, self.end, 3)

# Set up GUI
mainLabel = gui.elements.UILabel(relative_rect = pygame.Rect((3 * width / 8, 7 * height / 16, width / 4, height / 8)), text = "J.A.R.V.I.S", manager = manager, object_id = "#main_label")
arcs = [
    Arc(0, 4, 1, 3), Arc(math.pi, 4, 1.5, 3), Arc(1, -4, 0.5, 3), Arc(math.pi / 5, -10, math.pi / 12, 3),
    Arc(math.pi / 2, -6, math.pi / 4, 2), Arc(3 * math.pi / 2, -6, 1.2, 2), Arc(math.pi / 5, 10, math.pi / 12, 2), Arc(6 * math.pi / 5, 10, math.pi / 10, 2),
    Arc(1, 5, 0.8, 1), Arc(math.pi + 1, 5, 0.8, 1)
]

wavePos = 0
waveSpeed = math.radians(100)
ticks = []
numTicks = 50
for i in range(numTicks):
    ticks.append(Tick(i * (2 * math.pi / numTicks)))

mainPanel = gui.elements.UIPanel(relative_rect = pygame.Rect((0, 0, width / 15, height)), manager = manager, object_id = "#panel")

manualInputButton = gui.elements.UIButton(relative_rect = pygame.Rect((0, 10, width / 20, width / 20)), text = "+", manager = manager, container = mainPanel, anchors = {"centerx" : "centerx"}, object_id = "#button")
manualToggle = False

manualInputPanel = gui.elements.UIPanel(relative_rect = pygame.Rect((width / 15 + 5, 5, width / 6, height / 5)), manager = manager, object_id = "#panel")
manualInputText = gui.elements.UILabel(relative_rect = pygame.Rect((0, 5, width / 9, height / 20)), text = "Manual Input", manager = manager, container = manualInputPanel, object_id = "#text", anchors = {"centerx" : "centerx"})
manualInput = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((0, 0, width / 9, height / 20)), manager = manager, container = manualInputPanel, object_id = "#text_entry", anchors = {"centerx" : "centerx", "centery" : "centery"})

manualCalculateButton = gui.elements.UIButton(relative_rect = pygame.Rect((0, width / 20 + 20, width / 20, width / 20)), text = "+", manager = manager, container = mainPanel, anchors = {"centerx" : "centerx"}, object_id = "#button")
calculateToggle = False

manualCalculatePanel = gui.elements.UIPanel(relative_rect = pygame.Rect((width / 15 + 5, 5, width / 6, height / 5)), manager = manager, object_id = "#panel")
manualCalculateText = gui.elements.UILabel(relative_rect = pygame.Rect((0, 5, width / 9, height / 20)), text = "Calculator", manager = manager, container = manualCalculatePanel, object_id = "#text", anchors = {"centerx" : "centerx"})
manualCalculate = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((0, 0, width / 9, height / 20)), manager = manager, container = manualCalculatePanel, object_id = "#text_entry", anchors = {"centerx" : "centerx", "centery" : "centery"})

notificationPanel = gui.elements.UIPanel(relative_rect = pygame.Rect((-(width / 5), 10, width / 5, height / 10)), manager = manager, object_id = "#panel", anchors = {"right" : "right", "top" : "top"})
notificationText = gui.elements.UILabel(relative_rect = pygame.Rect((0, 0, width / 5, height / 10)), text = "", manager = manager, container = notificationPanel, object_id = "#text")
notificationState = "hidden"
progress = 0
time = 0

def updateGUI():
    global progress
    global time
    global notificationState
    global waveSpeed
    global wavePos

    if state.talking:
        waveSpeed = -math.radians(400)
    else:
        waveSpeed = math.radians(100)
    wavePos += waveSpeed * dt
    wavePos %= (2 * math.pi)

    for tick in ticks:
        tick.update()

    mainLabel.set_relative_position((3 * width / 8, 7 * height / 16))
    mainLabel.set_dimensions((width / 4, height / 8))
    mainPanel.set_dimensions((width / 15, height + 20))

    manualInputButton.set_dimensions((width / 20, width / 20))
    if manualToggle:
        manualInputButton.set_text("-")
        manualInputPanel.show()
        manualCalculatePanel.set_relative_position((width / 15 + 5, height / 5 + 10))
    else:
        manualInputButton.set_text("+")
        manualInputPanel.hide()
        manualCalculatePanel.set_relative_position((width / 15 + 5, 5))

    manualInputPanel.set_relative_position((width / 15 + 5, 5))
    manualInputPanel.set_dimensions((width / 6, height / 5))
    manualCalculatePanel.set_dimensions((width / 6, height / 5))
    manualInput.set_dimensions((width / 9, height / 20))
    manualCalculate.set_dimensions((width / 9, height / 20))
    manualInputText.set_dimensions((width / 9, height / 20))
    manualCalculateText.set_dimensions((width / 9, height / 20))


    manualCalculateButton.set_dimensions((width / 20, width / 20))
    manualCalculateButton.set_relative_position((0, width / 20 + 20, width / 20, width / 20))
    if calculateToggle:
        manualCalculateButton.set_text("-")
        manualCalculatePanel.show()
    else:
        manualCalculateButton.set_text("+")
        manualCalculatePanel.hide()

    gap = height // 12
    for radius in range(2, 5, 1):
        if state.currentState == "Error":
            colour = secondaryWarningColour
        else:
            colour = secondaryColour
        pygame.draw.circle(screen, colour, (width // 2, height // 2), radius * gap, 2)

    for arc in arcs:
        arc.update()

    if notificationState == "hidden":
        notificationPanel.hide()
        notificationPanel.set_relative_position((-10, 10))
        progress = 0
    elif notificationState == "entering":
        notificationPanel.show()
        notificationPanel.set_relative_position((-10 + (-(width / 5) + 10) * (1 - (1 - progress) ** 6), 10))
        progress += dt 
        if progress >= 1:
            notificationState = "holding"
            progress = 0
    elif notificationState == "holding":
        time += dt
        if time >= holdTime:
            notificationState = "hidden"
            time = 0

    if state.justChanged:
        if state.currentState == "Searching":
            notification("Searching...")
        state.justChanged = False

def notification(text):
    global notificationState
    notificationText.set_text(text)
    notificationState = "entering"

def handleEvent(event):
    if event.type == gui.UI_BUTTON_PRESSED:
        if event.ui_element == manualInputButton:
            global manualToggle
            manualToggle = not manualToggle
        elif event.ui_element == manualCalculateButton:
            global calculateToggle
            calculateToggle = not calculateToggle
    elif event.type == gui.UI_TEXT_ENTRY_FINISHED:
        if event.ui_element == manualInput:
            text = event.text
            manualInput.set_text("")
            thread = threading.Thread(target = VoiceAssistant.process, args = (text,))
            thread.start()
        elif event.ui_element == manualCalculate:
            text = event.text
            manualCalculate.set_text("")
            thread = threading.Thread(target = Calculate.calculator, args = (text,))
            thread.start()

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = screen.get_width(), screen.get_height()
            manager.set_window_resolution((width, height))
        else:
            handleEvent(event)
            manager.process_events(event)

    screen.fill(backgroundColour)

    # Render GUI
    updateGUI()
    manager.update(dt)

    manager.draw_ui(screen)
    pygame.display.flip()
    
pygame.quit()