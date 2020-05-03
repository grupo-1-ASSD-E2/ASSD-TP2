#UTIL: KS in python https://flothesof.github.io/Karplus-Strong-algorithm-Python.html
import numpy as np
#from IPython.display import Audio
#from moviepy.editor import VideoClip
#from moviepy.video.io.bindings import mplfig_to_npimage
#import simpleaudio as sa
import pyaudio



# class KS_Synthesizer ():
#     def __init__(self, in_rl = 0.5, in_l = 0, fs = 500):
#         rl = in_rl
#         l = in_l
#         f_note = fs / (l + 0.5)

# rl = 0.8
# l = 
# f_note = fs / (l + 0.5)

# def noise_generator():
#     return 1 #hacer

# x
# x_1
# y_l
# y_l_1

# def play_nT(midi_file, fs, n, rl, x, x_1, y_l, y_l_1):
#     T = 1/fs
# x = 
# m = n * T
# y = 0.5 * (x + x_1 + rl * (y_l + y_l_1))

fs = 8000
t = np.linspace(0, 1, num=fs)
wavetable = np.sin(np.sin(2 * np.pi * t)) #sinusoidal

def synthesize(sampling_speed, wavetable, n_samples):
    """Synthesizes a new waveform from an existing wavetable."""
    samples = []
    current_sample = 0
    while len(samples) < n_samples:
        current_sample += sampling_speed
        current_sample = current_sample % wavetable.size
        samples.append(wavetable[current_sample])
        current_sample += 1
    return np.array(samples)

sample1 = synthesize(220, wavetable, 2 * fs)
sample2 = synthesize(440, wavetable, 2 * fs)

#Audio(sample1, rate=fs)

signal = np.random.random(750)
#Audio(signal, rate=250)
print('nro de bytes de sample 1')
print(sample1.itemsize)
#play_obj = sa.play_buffer(sample1, 1, sample1.itemsize , fs)
#play_obj.wait_done()

#-----------------


fs = 8000
t = np.linspace(0, 1, num=fs)
wavetable = np.sin(np.sin(2 * np.pi * t)) #sinusoidal

def synthesize(sampling_speed, wavetable, n_samples):
    """Synthesizes a new waveform from an existing wavetable."""
    samples = []
    current_sample = 0
    while len(samples) < n_samples:
        current_sample += sampling_speed
        current_sample = current_sample % wavetable.size
        samples.append(wavetable[current_sample])
        current_sample += 1
    return np.array(samples)

sample1 = synthesize(220, wavetable, 2 * fs)
sample2 = synthesize(440, wavetable, 2 * fs)

Audio(sample1, rate=fs)

#----------------------

# volume range [0.0, 1.0]
# f sine frequency, Hz, may be float
# phase in radians
def get_sine_wave(volume, f, phase=0, cos=False):
    if cos == False:
        y = np.sin(f * 2 * np.pi * t +phase)  # Has frequency of 440Hz
    else:
        y = np.cos(f * 2 * np.pi * t + phase)
        # Ensure that highest value is in 16-bit range
    audio = volume * y * (2 ** 15 - 1) / np.max(np.abs(y))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    return audio


# To reproduce sine waves

def play_sine_wave(audio):

    # Start playback
    #sa.play_buffer:
    #audio_data – object with audio data (must support the buffer interface)
    #num_channels (int) – the number of audio channels
    #bytes_per_sample (int) – the number of bytes per single-channel sample
    #sample_rate (int) – the sample rate in Hz
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()