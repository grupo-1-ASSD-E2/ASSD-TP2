from audio_efects.Reverberation.reverb import Reverb
from matplotlib import pyplot as plt
import numpy as np

audio_filter = Reverb(44100)
h1, h2, h3, h4, h5, h6 = audio_filter.__get_filters_response_debug__()

x = np.arange(len(h1))
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h1, colors='g')
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h2, colors='r')
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h3, colors='b')
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h4, colors='y')
plt.show()

plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h6, colors='b')
plt.vlines(x, ymin=np.zeros(len(h1)), ymax=h5, colors='y')
plt.show()
