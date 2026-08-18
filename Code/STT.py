import sounddevice as sd
import numpy as np
import json
from vosk import Model, KaldiRecognizer
import threading
import VoiceAssistant
from State import state

rate = 16000

model = Model("models/vosk-model-small-en-us-0.15")

def listen():
    chunks = []

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        chunks.append(indata.copy())

    recogniser = KaldiRecognizer(model, rate)

    stream = sd.InputStream(samplerate = rate, channels = 1, dtype = "float32", callback = callback)
    stream.start()
    while state.listening: pass
    stream.stop()
    stream.close()

    recording = np.concatenate(chunks, axis = 0)

    # float32 gives between -1.0 and 1.0
    # Vosk wants int16 (-32768 to 32767)
    scaled = (recording * 32767).astype("int16")
    byteData = scaled.tobytes()

    recogniser.AcceptWaveform(byteData)
    result = json.loads(recogniser.FinalResult())

    thread  = threading.Thread(target = VoiceAssistant.process, args = (result["text"],))
    thread.start()
