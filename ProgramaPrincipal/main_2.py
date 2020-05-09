from BackEnd.AudioEfects.Reverberation.Reverb import Reverb
from BackEnd.AudioEfects.Flanger.Vibrato import Vibrato
from matplotlib import pyplot as plt
import numpy as np


audio_filter = Vibrato(44100, 44100)
h1 = audio_filter.get_impulse_response()

x = np.arange(len(h1))
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h1, colors='g')

plt.show()

