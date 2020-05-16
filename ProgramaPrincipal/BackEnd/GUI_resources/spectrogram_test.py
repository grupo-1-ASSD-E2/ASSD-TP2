from spectrogram_plotter import Spectrogrammer, PyQtPlotter
import matplotlib.pyplot as plt
import numpy as np


spectro = Spectrogrammer()
# This line requires a file too heavy for committing, ask and it will be given, but you'll not find it in the repo.
br = np.load('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP2/ProgramaPrincipal/BackEnd/GUI_resources/Bohemian Rhapsody ndarray.npy')
br = br[:2**18]
ts = 1 / 44100
time_array = np.arange(0, ts*br.size, ts, dtype=br.dtype)
spectro.compute_audio_array(time_array, br)
spectro.calculate_FFTs()
mag = spectro.get_FFTs_magnitude()
time = spectro.get_resampled_time_array()
freq = spectro.get_FFTs_freq()

plotter = PyQtPlotter()
plotter.spectrogram(time, freq, mag)

x_time, y_freq = np.meshgrid(time, freq)
plt.pcolor(x_time, np.fft.fftshift(y_freq), np.fft.fftshift(mag.T), vmin=-100, vmax=mag.max(), cmap='coolwarm')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar(label='Magntud (dB)')
plt.semilogy()
plt.ylim(bottom=1e1, top=2e4)
plt.show()