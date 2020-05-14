from BackEnd.AudioEfects.Reverberation.Eco import EcoSimple
from BackEnd.AudioEfects.Reverberation.LowPassReverb import LowPassReverb
from BackEnd.AudioEfects.Reverberation.PlainPeverb import PlainReverb
from BackEnd.AudioEfects.Reverberation.AllPassReverb import AllPassReverb
from BackEnd.AudioEfects.Reverberation.Reverb import Reverb
from BackEnd.AudioEfects.convolutioner import Convolutioner
from BackEnd.AudioEfects.Flanger.Vibrato import Vibrato
from BackEnd.AudioEfects.Flanger.Flanger import Flanger
import matplotlib.pyplot as plt
import librosa
import numpy as np
from multiprocessing import Pool
import time
from scipy.io.wavfile import write


def hola(a, b):
    return b(a)

def foo1(a):
    return a

def foo2(a):
    b = np.ones(len(a))
    return b


my_array = np.array([([1,1],[2,2]),([1,1],[2,2]),([1,1],[2,2]) ])
print(my_array[:,1])


"""
new_data, new_rate = librosa.load('D:\\santi\\facultad\\3ero\\2do cuatri\\ASSD\\GIT\\ASSD-TP2\\ProgramaPrincipal\\Resources\\hola.wav',
                                  sr=44100)
print(len(new_data))
x = np.arange(0, len(new_data))
x = x/44100.0
a = 2**15
eco = Reverb(buffer_len=a, t_60=10)
eco1 = PlainReverb(buffer_len=a)
conv = Convolutioner(frame_count=a)
vibrato = Vibrato(buffer_len=a)
flan = Flanger(buffer_len=a)
conv.update_input(new_data, np.dtype('float32'))
conv.custom_processing_callback(flan.compute)
conv.set_mixing_gain(1)
conv.start_non_blocking_processing(frame_count=a)

while conv.processing():
    time.sleep(1)

input = conv.input_array[0]
out2 = conv.output_array.copy()
_x = np.arange(len(out2))/44100.0
plt.plot(np.arange(len(input))/44100.0, input)
plt.plot(_x, out2)

plt.show()

#write('my_file.wav', 44100, np.int16(out2*32767))
#conv.get_output_file('D:\\santi\\facultad\\3ero\\2do cuatri\\ASSD\\GIT\\ASSD-TP2\\ProgramaPrincipal\\Resources\\hola_bueno.mp3',
                     #44100)

def compute(smaple, index):
"""
