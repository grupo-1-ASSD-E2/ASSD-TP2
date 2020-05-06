
import pyaudio
import numpy as np
#from ProgramaPrincipal.BackEnd.KarplusStrongSynthesis.KS_Synthesizer import KS_Synthesizer as KS
#import ProgramaPrincipal.BackEnd.KarplusStrongSynthesis.KS_Synthesizer as KS
from KS_Synthesizer import KS_Synthesizer
import KS_Synthesis as KS



fs = 44100
note_freq = 440
ks = KS.KS_Synthesizer()
signal = KS.get_note_signal(fs,note_freq)
