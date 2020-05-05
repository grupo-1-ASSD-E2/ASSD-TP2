#UTIL: KS in python https://flothesof.github.io/Karplus-Strong-algorithm-Python.html
import numpy as np
#from IPython.display import Audio
#from moviepy.editor import VideoClip
#from moviepy.video.io.bindings import mplfig_to_npimage
#import simpleaudio as sa
import pyaudio



class KS_Synthesizer ():
    # def __init__(self, in_rl = 0.5, in_l = 0, fs = 500):
    #     rl = in_rl
    #     l = in_l
    #     f_note = fs / (l + 0.5)
    def __init__(self):
        self.L = 150/440

    
    def get_note_signal(self, fs, note_freq):
        self.L = np.rint((fs / note_freq) - 0.5)
        print ('L:', self.L)
        self.wavetable = (2 * np.random.randint(0, 2, (self.L)+1) - 1).astype(np.float)
        self.rl = 0.95
        self.y = self.karplus_strong(fs, self.L, self.rl, self.wavetable)
        

    def karplus_strong(self, fs, L, rl, wavetable):
        self.awgn = np.random.normal(0,1,(self.L)+1)
        self.x = self.awgn
        print('awgn:', self.awgn)
        print('awgn length:', len(self.awgn))
        self.y = [L]
        for k in L:
            self.y[k]= 0.5 * (self.x[k+1] + self.x[k]) + 0.5 * rl * (wavetable[k+1] + wavetable[k])
        return self.y






         

