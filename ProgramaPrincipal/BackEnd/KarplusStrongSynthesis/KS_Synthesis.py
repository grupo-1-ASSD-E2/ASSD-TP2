import numpy as np
import pyaudio
import simpleaudio as sa
import random

from BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np
import time

class KS_Synthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def create_note_signal(self, note, instrument):
        if instrument == 'Guitar':
            self.karplus_strong(note)
        elif instrument == 'Drum':
            self.karplus_strong_Extended(note)


    def karplus_strong(self, note):
        N = np.linspace(0, note.duration, int(round(note.fs * note.duration)))
        rl = 0.9995
        L = int(np.rint((note.fs / note.frequency) - 0.5))
        wavetable = (2 * np.random.randint(0, 2, L+2) - 1).astype(np.float) #va L+1
        sample_k = 0
        y = []
        for k in range(N.size):
            if k <= L:
                sample_k = 0.5 * rl * (wavetable[k+1] + wavetable[k])
            else:
                sample_k = 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        note.output_signal = np.array(y)

    def karplus_strong_extended(self, note):
        i=1





    # def ks(self, fs, note_freq, note_duration):
    #     N = np.linspace(0, note_duration, num=(fs * note_duration))
    #     rl = 1
    #     L = int(np.rint((fs / note_freq) - 0.5))
    #     wavetable = (2 * np.random.randint(0, 2, L+2) - 1).astype(np.float) #va L+1
    #     sample_k = 0
    #     y = []
    #     for k in range(N.size):
    #         if k <= L:
    #             sample_k = 0.5 * rl * (wavetable[k+1] + wavetable[k])
    #         else:
    #             sample_k = 0.5 * rl * (y[k-L] + y[k-L-1])
    #         y.append(sample_k)
    #     return np.array(y)

