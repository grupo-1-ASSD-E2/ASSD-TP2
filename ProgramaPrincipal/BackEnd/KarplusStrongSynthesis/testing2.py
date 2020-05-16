
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import control
from scipy import signal



octava0 = 27.5, 29.135, 30.868
octava1 = 32.703, 34.648, 36.708, 38.891, 41.203, 43.654, 46.249, 48.999, 51.913, 55.000, 58.270, 61.735
octava2 = 65.406, 69.296, 73.416, 77.782, 82.407, 87.307, 92.499, 97.999, 103.826, 110.000, 116.541, 123.471
octava3 = 130.813, 138.591, 146.832, 155.563, 164.814, 174.614, 184.997, 195.998, 207.652, 220.000, 233.082, 244.942
octava4 = 261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440.000, 466.164, 493.883
octava5 = 523.251, 554.365, 587.330, 622.254, 659.255, 698.456, 739.989, 783.991, 830.609, 880.000, 932.328, 987.767
octava6 = 1046.502, 1108.731, 1174.659, 1244.508, 1318.510, 1396.913, 1479.978, 1567.982, 1661.219, 1760.000, 1864.655, 1975.533
octava7 = 2093.005, 2217.461, 2349.318, 2489.016, 2637.020, 2793.826, 2959.955, 3135.963, 3322.438, 3520.000, 3729.310, 3951.066
octava8 = 4186.009, 4434.922, 4698.636, 4978.032, 5274.041, 5587.652, 5919.911, 6271.927, 6644.875, 7040.000

fs = 44100
freq = 440
duration = 0.5

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1 #A MI ME ANDA CON 2 PERO PUEDE SER QUE A OTRO LE FUNCIONE CON 1!!
                )


def karplus_strong(duration,fs,frequency):
        N = np.linspace(0, duration, int(round(fs * duration)))
        r = 0.999
        L = int((fs / frequency) - 0.5)
        print('freq', frequency)
        print('L', L)
        rl = 0.999
        wavetable = (2 * np.random.randint(0, 2, L+2) - 1).astype(np.float) #va L+1
        sample_k = 0
        y = []
        delta = (fs/frequency) - 0.5 - L
        print('delta',delta)
        a = 1 - (delta/(1+delta))
        print('a',a)
        for k in range(N.size):
            if k <= (L + 1):
                sample_k = wavetable[k]
            else:
                sample_k = 0.5 * rl * y[k-L-2] + 0.5 * rl * (a+1) * y[k-L-1] + 0.5 * a * rl * y[k-L] - a * y[k-1]
            y.append(sample_k)
        return np.array(y)

def ks_basico(duration,fs,frequency):
        N = np.linspace(0, duration, int(round(fs * duration)))
        r = 0.999
        L = int((fs / frequency) - 0.5)
        rl = r**L
        wavetable = np.random.normal(0,1,L+2)#(2 * np.random.randint(0, 2, L+2) - 1).astype(np.float) #va L+1
        sample_k = 0
        y = []
        for k in range(N.size):
            if k <= L:
                sample_k = 0.5 * rl * (wavetable[k+1] + wavetable[k])
            else:
                sample_k = 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        return np.array(y)

def ks_basico_xnormal(duration,fs,frequency):
        N = np.linspace(0, duration, int(round(fs * duration)))
        r = 0.999
        L = int((fs / frequency) - 0.5)
        rl = r**L
        wavetable = np.random.normal(0,1,L+2)
        sample_k = 0
        y = []
        for k in range(N.size):
            if k <= L:
                sample_k = 0.5 * rl * (wavetable[k+1] + wavetable[k])
            else:
                sample_k = 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        return np.array(y)

def ks_basico_xuniform(duration,fs,frequency):
        N = np.linspace(0, duration, int(round(fs * duration)))
        r = 0.999
        L = int((fs / frequency) - 0.5)
        rl = r**L
        wavetable = np.random.uniform(-1,1,L+2)
        sample_k = 0
        y = []
        for k in range(N.size):
            if k <= L:
                sample_k = 0.5 * rl * (wavetable[k+1] + wavetable[k])
            else:
                sample_k = 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        return np.array(y)

def karplus_strong_extended(duration, fs, frequency, b):
        N = np.linspace(0, duration * 10, int(round(fs * duration)))
        rl = 0.9995
        L = int(np.rint((fs / frequency) - 0.5))
        wavetable = (2 * np.random.randint(0, 2, L+2) - 1).astype(np.float)
        sample_k = 0
        y = []
        for k in range(N.size):
            r = np.random.binomial(1, b)
            sign = float(r == 1) * 2 - 1
            if k <= L:
                sample_k = sign * 0.5 * rl * (wavetable[k+1] + wavetable[k])
            else:
                sample_k = sign * 0.5 * rl * (y[k-L] + y[k-L-1])
            y.append(sample_k)
        return np.array(y)


#PARA PROBAR GUITARRA
'''
for freq in octava0:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava1:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava2:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())    
for freq in octava3:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava4:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava5:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava6:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava7:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
for freq in octava8:
    sample1 = karplus_strong(duration,fs,freq)
    stream.write(sample1.astype(np.float32).tostring())
'''

#PARA PROBAR DRUMS
'''
for freq in freqs0:#BIEN
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs1:#BIEN
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs2: #BIEN
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())  
for freq in freqs3:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs4:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs5:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs6:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs7:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
for freq in freqs8:
    sample1 = karplus_strong_extended(duration,fs,freq,0.5)
    stream.write(sample1.astype(np.float32).tostring())
'''

#PARA COMPARAR RUIDO NORMAL VS UNIFORME




sample = karplus_strong(1,fs,220)
sample2 = ks_basico(1,fs,220)
sample3 = ks_basico_xnormal(1,fs,440)
sample4 = ks_basico_xuniform(1,fs,440)
stream.write(sample.astype(np.float32).tostring())
#stream.write(sample2.astype(np.float32).tostring())


#plt.title('Decaimiento temporal del sonido')
plt.subplot(211)
plt.plot(sample3, label='x(n) ruido normal')
plt.subplot(211)
plt.plot(sample4, label='x(n) ruido uniforme')
plt.xlim(0, sample.size)
plt.legend()
plt.subplot(212)
#plt.plot(sample)
plt.subplot(212)
plt.plot(sample3, label='x(n) ruido normal')
plt.subplot(212)
plt.plot(sample4, label='x(n) ruido uniforme')
plt.xlim(0, 1000)
plt.xlabel('n')
plt.ylabel('y(n)')
#axs[0].set_legend('curva1')
plt.legend()
plt.show()

#h = signal.TransferFunctionDiscrete(array([0.5]))

'''
def plot_h():
    f,ax=plt.subplots()
    z = np.linspace(0, np.pi, 10000)
    rl = 0.999
    l = 99
    h = (0.5 + 0.5 * z**(-1)) / (1 - 0.5 * rl * z**(-l) - 0.5 * rl * z**(-1-l))
    #.plot(z,h)
    ax.plot(z/np.pi,h)
    ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
    plt.xlabel()
    plt.show()

def plot_fft():
    y = ks_basico(1,44100,7040)
    fft = np.fft.fft(y,2**16)
    #plt.plot(np.abs(fft)/(2**16))
    f = np.fft.fftfreq(2**16, 1/44100)
    plt.plot(np.fft.fftshift(f),np.fft.fftshift(20*np.log10(np.abs(fft)/(2**16))))
    plt.xlim(0,20000)
    #plt.ylim(0,0.08)
    plt.grid(which='both')
    plt.xlabel('f[Hz]')
    plt.ylabel('Magnitude[dB]')
    plt.show()

#plot_h()
plot_fft()
'''



