#INFO: https://flothesof.github.io/Karplus-Strong-algorithm-Python.html
import pyaudio
import numpy as np


fs = 44100
t = np.linspace(0, 0.5, num=fs)


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

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer=1024,
                output=True,
                output_device_index=2 #A MI ME ANDA CON 2 PERO PUEDE SER QUE A OTRO LE FUNCIONE CON 1!!
                )

#------------------------------
#WAVETABLE: Tones are periodic. The following are different types of wavetables.

wavetable = np.sin(np.sin(2 * np.pi * t)) #sinusoidal
sample1 = synthesize(220, wavetable, 2 * fs)
sample2 = synthesize(440, wavetable, 2 * fs)
stream.write(sample1.astype(np.float32).tostring())
stream.write(sample2.astype(np.float32).tostring())
#stream.close()

#------------------------------
wavetable = t * (t < 0.5) + (-(t - 1)) * (t>= 0.5) #triangular
sample1 = synthesize(220, wavetable, 2 * fs)
sample2 = synthesize(440, wavetable, 2 * fs)
stream.write(sample1.astype(np.float32).tostring())
stream.write(sample2.astype(np.float32).tostring())
#stream.close()

#------------------------------
def make_sine_wavetable(n_samples, amps, phases, freqs): #to get a more complex sinusoidal
    """Makes a wavetable from a sum of sines."""
    t = np.linspace(0, 1, num=n_samples)
    wavetable = np.zeros_like(t)
    for amp, phase, freq in zip(amps, 
                                phases,
                                freqs):
        wavetable += amp * np.sin(np.sin(2 * np.pi * freq * t + phase)) + \
                         amp / 2 * np.sin(np.sin(2 * np.pi * 2 * freq * t + phase))
    return wavetable

wavetable = make_sine_wavetable(t.size, [0.1, 0.5, 0.8, 0.3], #the more complex sinusoidal
                            [0, 0.3, 0.4, 0.7],
                            [1, 2.1, 3, 4.3])

sample1 = synthesize(220, wavetable, 2 * fs)
sample2 = synthesize(440, wavetable, 2 * fs)
stream.write(sample1.astype(np.float32).tostring())
stream.write(sample2.astype(np.float32).tostring())
#stream.close()

#------------------------------
#KARPLUS-STRONG: The wavetable changes.

def karplus_strong(wavetable, n_samples):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
    samples = []
    current_sample = 0
    previous_value = 0
    while len(samples) < n_samples:
        wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)

#Para una frecuencia determinada
wavetable_size = fs // 55 
wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
sample1 = karplus_strong(wavetable, 2 * fs)
#stream.write(sample1.astype(np.float32).tostring())


#Para una frecuencia mayor
wavetable_size = fs // 110 
wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
sample2 = karplus_strong(wavetable, 2 * fs)
stream.write(sample2.astype(np.float32).tostring())


wavetable_size = fs // 220 
wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
sample3 = karplus_strong(wavetable, 2 * fs)
stream.write(sample3.astype(np.float32).tostring())


wavetable_size = fs // 440 
wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
sample4 = karplus_strong(wavetable, 2 * fs)
stream.write(sample4.astype(np.float32).tostring())


wavetable_size = fs // 880 
wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
sample5 = karplus_strong(wavetable, 2 * fs)
stream.write(sample5.astype(np.float32).tostring())


#---------------------------
freqs = np.logspace(0, 1, num=10, base=2) * 55
for freq in freqs:
    wavetable_size = fs // int(freq)
    wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
    sample = karplus_strong(wavetable, 1 * fs)
    stream.write(sample.astype(np.float32).tostring())

waveforms = []
for ind, freq in enumerate(freqs):
    wavetable_size = fs // int(freq)
    wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
    sample = karplus_strong(wavetable, 2 * fs)
    waveforms.append(sample)
    stream.write(sample.astype(np.float32).tostring())

#-------------------------
#KARPLUS-STRONG (EXTENSION) FOR DRUM 
def karplus_strong_drum(wavetable, n_samples, prob):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
    samples = []
    current_sample = 0
    previous_value = 0
    while len(samples) < n_samples:
        r = np.random.binomial(1, prob)
        sign = float(r == 1) * 2 - 1
        wavetable[current_sample] = sign * 0.5 * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)

wavetable_size = fs // 40 
wavetable = np.ones(wavetable_size)
sample1 = karplus_strong_drum(wavetable, 1 * fs, 0.3)
stream.write(sample1.astype(np.float32).tostring())

#Changing b parameter
bs = np.arange(0, 1.1, 0.1)
for b in bs:
    wavetable = np.ones(wavetable_size)
    sample = karplus_strong_drum(wavetable, 1 * fs, b)
    stream.write(sample.astype(np.float32).tostring())

#For b=0
fs = 20000
for freq in [20, 55, 110, 220, 440, 880, 1288]:
    wavetable_size = fs // freq 
    wavetable = np.ones(wavetable_size)
    sample = karplus_strong_drum(wavetable, 2 * fs, 0)
    stream.write(sample.astype(np.float32).tostring())

#To get longer delays:
# def karplus_strong_decay(wavetable, n_samples, stretch_factor):
#     """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging.
#     Uses a stretch_factor to control for decay."""
#     samples = []
#     current_sample = 0
#     previous_value = 0
#     while len(samples) < n_samples:
#         r = np.random.binomial(1, 1 - 1/stretch_factor)
#         if r == 0:
#             wavetable[current_sample] =  0.5 * (wavetable[current_sample] + previous_value)
#         samples.append(wavetable[current_sample])
#         previous_value = samples[-1]
#         current_sample += 1
#         current_sample = current_sample % wavetable.size
#     return np.array(samples)

# fs = 44100
# stretch_factors = [1, 2.1, 3.5, 4, 8]
# freq = 220
# waveforms = []
# for ind, stretch_factor in enumerate(stretch_factors):
#     wavetable_size = fs // int(freq)
#     wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
#     sample = karplus_strong_decay(wavetable, 2 * fs, stretch_factor)
#     waveforms.append(sample)
# for waveform in waveforms:
    #stream.write(sample.astype(np.float32).tostring())

#------------------------
#Este no me gusto nada
# wavetable_size = fs // int(freq)
# wavetable = make_sine_wavetable(wavetable_size, [0.3, 0.5, 0.3], [0, 0.5, 0], [1, 3, 9])
# sample = karplus_strong_decay(wavetable, 5 * fs, stretch_factor=20)
#stream.write(sample.astype(np.float32).tostring())

stream.close()