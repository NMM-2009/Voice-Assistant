import asyncio
import edge_tts as tts
import pygame.mixer as mixer
from State import state

async def generateSpeech(text, output_file = "output.mp3"):
    voice = "en-GB-RyanNeural"
    communicate = tts.Communicate(text, voice)
    await communicate.save(output_file)

def speak(text):
    mixer.init()
    asyncio.run(generateSpeech(text))
    mixer.music.load("output.mp3")
    state.talking = True
    mixer.music.play()
    while mixer.music.get_busy(): pass
    state.talking = False
