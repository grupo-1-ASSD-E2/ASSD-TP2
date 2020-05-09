import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import fftpack


fs_rate, signal = wavfile.read("ProgramaPrincipal/BackEnd/AdditiveSynthesis/acc-c4.wav")


N = signal.shape[0]
secs = N / float(fs_rate)
Ts = 1.0 / fs_rate
t = scipy.arange(0, secs, Ts)
fftobtained = scipy.fft(signal)
FFT = abs(fftobtained)
FFT_side = FFT[range(N // 2)]
freqs = scipy.fftpack.fftfreq(signal.size, t[1] - t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N // 2)]
fft_freqs_side = np.array(freqs_side)

maxmax = np.max(FFT)
maxsignal = np.max(signal)

harmonics = []
phases = []



def iterate(n):
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 7))

    for i in range(n, n+5):
        high_freq_fft = fftobtained.copy()
        high_freq_fft[np.abs(freqs) >( 270 * i)] = 0
        high_freq_fft[np.abs(freqs) < 250 * i] = 0
        filtered_sig = fftpack.ifft(high_freq_fft)

        axes[i - n, 0].plot(freqs, abs(high_freq_fft) / maxmax)
        axes[i -n, 1].plot(t, filtered_sig / maxsignal)
        axes[i-n, 0].set_xlabel("i" + str(i))
        index = np.argmax(abs(high_freq_fft))
        fmax = freqs[index]
        pmax = np.angle(fftobtained[index])

        harmonics.append(fmax)
        phases.append(pmax)

    print(harmonics)
    print(phases)

    fig.tight_layout()
    plt.show()

    i = 0

def plot_once():
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 7))
    # plot time signal:
    #axes[0].set_title("Signal")
    axes[0].plot( t,signal, color='C0')
    
    axes[0].set_title("Time signal")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlabel("Time (s)")

    # plot different spectrum types:
    axes[1].set_title("Freq Spectrum")
    axes[1].magnitude_spectrum(signal, Fs=fs_rate, color='C1')
    axes[1].set_xlabel("Freq (f)")

    axes[2].set_title("Phase Spectrum ")
    axes[2].phase_spectrum(signal, Fs=fs_rate, color='C2')
    axes[2].set_xlabel("Freq (f)")

    fig.tight_layout()
    plt.show()


plot_once()
#iterate(1)
#iterate(6)
iterate(16)
