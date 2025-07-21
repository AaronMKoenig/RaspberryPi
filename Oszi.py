import pyaudio 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

yAxis = 20000  # Y-Achsen-Skalierung für das Oszilloskop

class Oszi:
    def __init__(self, rate=48000, channels=1, chunk_size=1024):
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)

    def read_data(self):
        data = self.stream.read(self.chunk_size)
        return np.frombuffer(data, dtype=np.int16)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

oszi = Oszi()

fig, ax = plt.subplots()
x = np.arange(0, oszi.chunk_size)
line, = ax.plot(x, np.zeros(oszi.chunk_size))
ax.set_ylim(-yAxis, yAxis)  # Genauere Y-Achsen-Skalierung
ax.set_title("Live Mikrofon-Oszilloskop")
ax.set_xlabel("Samples")
ax.set_ylabel("Amplitude")

def update(frame):
    data = oszi.read_data()
    line.set_ydata(data)
    return line,

ani = animation.FuncAnimation(fig, update, interval=30)
try:
    plt.show()
finally:
    oszi.close()
