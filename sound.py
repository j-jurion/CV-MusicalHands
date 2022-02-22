import pyaudio
import numpy as np

class Sound():
  def __init__(self) -> None:
    self.p = pyaudio.PyAudio()
    print(self.p.get_default_output_device_info())

  def play(self, frequency, volume):
    fs = 48000       # sampling rate, Hz, must be integer
    duration = 1   # in seconds, may be float

    # generate samples, note conversion to float32 array
    self.samples = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    self.stream = self.p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)

    self.stream.write(volume*self.samples)

    #self.stream.stop_stream()
    #self.stream.close()

    #self.p.terminate()
