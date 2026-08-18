import sounddevice as sd
import numpy as np

chunks = []

def callback(indata, frames, time_info, status):
    if status:
        print(status)
    chunks.append(indata.copy())

stream = sd.InputStream(samplerate = 16000, channels = 1, dtype = "float32", callback = callback)

stream.start()
input("Recording... press Enter to stop")
stream.stop()

recording = np.concatenate(chunks, axis = 0)
