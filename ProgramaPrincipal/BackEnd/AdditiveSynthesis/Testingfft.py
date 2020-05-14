import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import fftpack
from scipy import signal as sig
import xlwt


fs_rate, signal = wavfile.read("ProgramaPrincipal/BackEnd/AdditiveSynthesis/trumpetnotes/trumpet-G5_783.99.wav")
book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

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
amplitudes = []


def iterate(n):
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 7))

    for i in range(n, n+5):
        high_freq_fft = fftobtained.copy()
        high_freq_fft[np.abs(freqs) >( 795 * i)] = 0
        high_freq_fft[np.abs(freqs) < 770* i] = 0
        filtered_sig = fftpack.ifft(high_freq_fft)

        axes[i - n, 0].plot(freqs, abs(high_freq_fft) / maxmax)
        axes[i -n, 1].plot(t, filtered_sig / maxsignal)
        axes[i-n, 0].set_xlabel("Parcial " + str(i))
        axes[i-n, 1].set_xlabel("Time (s) ")
        axes[i-n, 1].set_ylabel("Amplitude")
        index = np.argmax(abs(high_freq_fft))
        fmax = freqs[index]
        pmax = np.angle(fftobtained[index])
        amplitudemax = np.max(abs(high_freq_fft))


        sheet1.write(i, 0, str(fmax))
        sheet1.write(i, 1, str(amplitudemax/maxmax))
        

        amplitudes.append(amplitudemax/maxmax)
        harmonics.append(fmax)
        phases.append(pmax)

    print(harmonics)
    print(phases)
    #print(amplitudes)
    fig.tight_layout()
    plt.show()

    i = 0
def plot_once():

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(7, 7))
    # plot time signal:
    #axes[0].set_title("Signal")
    axes[0].plot( t,signal/np.max(signal), color='C0')
    
    axes[0].set_title("Trompeta")
    axes[0].set_ylabel("Amplitud")
    axes[0].set_xlabel("Tiempo (s)")

    # plot different spectrum types:
    axes[1].set_title("Análisis espectral")
    axes[1].magnitude_spectrum(signal, Fs=fs_rate, color='C1')
    axes[1].set_xlabel("Freq (Hz)")
    axes[1].set_ylabel("Energía")

    f2, t2, Sxx = sig.spectrogram(signal, fs_rate)
    axes[2].pcolormesh(t2, f2, Sxx)


    axes[2].set_title("Espectrograma ")
    #axes[2].plot(spec, Fs=fs_rate, color='C2')
    axes[2].set_xlabel("Tiempo (s)")
    axes[2].set_ylabel("Frecuencia (Hz)")
    fig.tight_layout()
    plt.show()


plot_once()

iterate(1)
iterate(6)

book.save("trial.xls")

#iterate(11)
