import PySimpleGUI as sg      
from pydub.generators import Sine
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import simpleaudio
import time

sr = 44100  # sample rate
bd = 16     # bit depth
l  = 100.0     # duration in millisec

silent = AudioSegment.silent(duration=1000)

class Sound():
  def __init__(self) -> None:
      self.play_obj = _play_with_simpleaudio(silent)

  def get_sine(self, freq):
    #create sine wave of given freq
    sine_wave = Sine(freq, sample_rate=sr, bit_depth=bd)

    #Convert waveform to audio_segment for playback and export
    sine_segment = sine_wave.to_audio_segment(duration=l)

    return sine_segment

  def play(self, freq):
    sound = self.get_sine(freq)
    #time.sleep(0.05)
    self.play_obj.stop()

    sound = sound.fade_in(1).fade_out(1)
    self.play_obj = _play_with_simpleaudio(sound)


