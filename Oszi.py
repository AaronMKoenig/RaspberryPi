import pyaudio 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import queue
import time

yAxis = 5000  # Y-Achsen-Skalierung für das Oszilloskop

class Oszi:
    def __init__(self, rate=48000, channels=1, chunk_size=512, device_index=None):
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   input_device_index=device_index,
                                   frames_per_buffer=self.chunk_size)
        self.running = True

    def read_data(self):
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        return np.frombuffer(data, dtype=np.int16)

    def close(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Geräte auflisten und auswählen
p = pyaudio.PyAudio()
print("Verfügbare Eingabegeräte:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info["maxInputChannels"] > 0:
        print(f"{i}: {info['name']}")
device_index = int(input("Bitte die Nummer des gewünschten Eingabegeräts eingeben: "))
p.terminate()

oszi = Oszi(device_index=device_index)
data_queue = queue.Queue(maxsize=10)

def record_thread():
    while oszi.running:
        data = oszi.read_data()
        try:
            data_queue.put(data, timeout=0.1)
        except queue.Full:
            pass  # Daten verwerfen, wenn die Queue voll ist

def plot_thread():
    fig, (ax_time, ax_freq) = plt.subplots(2, 1)
    x = np.arange(0, oszi.chunk_size)
    line_time, = ax_time.plot(x, np.zeros(oszi.chunk_size))
    ax_time.set_ylim(-yAxis, yAxis)
    ax_time.set_title("Live Mikrofon-Oszilloskop")
    ax_time.set_xlabel("Samples")
    ax_time.set_ylabel("Amplitude")

    xf = np.fft.rfftfreq(oszi.chunk_size, 1/oszi.rate)
    bars = ax_freq.bar(xf, np.zeros(len(xf)), width=xf[1]-xf[0])
    ax_freq.set_xlim(0, oszi.rate // 2)
    ax_freq.set_ylim(0, 10000)
    ax_freq.set_title("Frequenzspektrum (FFT)")
    ax_freq.set_xlabel("Frequenz [Hz]")
    ax_freq.set_ylabel("Amplitude")

    def update(frame):
        try:
            data = data_queue.get_nowait()
        except queue.Empty:
            data = np.zeros(oszi.chunk_size)
        line_time.set_ydata(data)
        yf = np.abs(np.fft.rfft(data))
        for bar, h in zip(bars, yf):
            bar.set_height(h)
        return [line_time] + list(bars)

    ani = animation.FuncAnimation(fig, update, interval=30)
    try:
        plt.tight_layout()
        plt.show()
    finally:
        oszi.close()

rec_thread = threading.Thread(target=record_thread, daemon=True)
rec_thread.start()

# plot_thread NICHT in einem eigenen Thread starten!
plot_thread()  # Das bleibt im Hauptthread
