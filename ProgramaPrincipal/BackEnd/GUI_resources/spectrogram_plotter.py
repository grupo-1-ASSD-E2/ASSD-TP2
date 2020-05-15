# Third-party modules
import scipy.signal as ss
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


class SpectroException(Exception):
    '''
    Exceptions for the Spectrogrammer class.
    '''
    def __init__(self, message=''):
        super().__init__()
        self.message = message



class Spectrogrammer():
    '''
    Calculates  FFTs of a size=self.frame_size and creates corresponding arrays to plot a spectrogram.

    'time_array' is the time points corresponding to the values of 'audio_array'.
    
    'audio_array' is the audio to perform the spectrogram. Can be any array-like object, but prefferably a numpy array of shape (N), where N is the amount of audio samples.
    N should be >= than 'frame_size'.

    'frame_size' is the amount of frames to be processed at a time (a.k.a. frames to pass to the FFT), prefferably a power of 2.
    If N is not a multiple of 'frame_size' (N = k*frame_size + R) where R is the size of the remaining samples, k FFTs will be computed, and the last R samples will
    be ignored.

    'dtype' is the data type to use. As default, the type of 'audio_array' will be used, and in that case, audio_array should be a numpy array.
    '''
    def __init__(self, time_array=np.array([]), audio_array=np.array([]), frame_size=2**10, dtype=None):
        if dtype is None:
            self.dtype = audio_array.dtype
        else:
            self.dtype = dtype

        self.compute_audio_array(np.array(audio_array, dtype=self.dtype), np.array(time_array, dtype=self.dtype))
        # Amount of frames to be processed at a time (a.k.a. frames to pass to the FFT), prefferably a power of 2.
        self.frame_size = frame_size
        
        # The FFTs will be stored here as ndarrays of shape (k, self.frame_size).
        self.FFTs = np.array([])
        self.freq = np.array([])


    def compute_audio_array(self, time_array, audio_array):
        # Time points corresponding to the values of 'audio_array'.
        self.time_array = time_array
        # Audio to perform the spectrogram.
        if len(audio_array.shape) == 1:
            self.audio_array = audio_array
        else:
            raise SpectroException('audio_array is not a 1-D array.')


    def calculate_FFTs(self):
        k = int(np.floor(self.audio_array.size / self.frame_size))
        audio_sliced = np.reshape(self.audio_array[:k*self.frame_size], (k, self.frame_size))
        self.FFTs = np.fft.fftn(audio_sliced)

        if self.time_array.size > 0:
            time_step = np.abs(self.time_array[1] - self.time_array[0])
            self.freq = np.fft.fftfreq(self.frame_size, d=time_step)

        return self.FFTs

    def get_FFTs_magnitude(self):
        try:
            my_abs = 20 * np.log10((np.abs(self.FFTs) / self.frame_size))
        except ZeroDivisionError:
            plt.plot(np.abs(self.FFTs))
            plt.show()

        return my_abs

    def get_FFTs_freq(self):
        return self.freq


    def get_resampled_time_array(self):
        return self.time_array[::self.frame_size]



class PyQtPlotter():
    '''
    Creates a PyQt5 figure to be displayed in an GUI.
    '''
    def __init__(self):
        # Variables to interact with Qt.
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)


    def spectrogram(self, time, freq, mag, title='Spectrogram', mag_min=None, mag_max=None, f_bottom=None, f_top=None):
        '''
        kwargs can be any of the supported by matplotlib.pyplot.pcolor
        '''
        if mag_min is None:
            mag_min_to_use = mag.min()
            mag_max_to_use = mag.max()
        else:
            mag_min_to_use = mag_min
            mag_max_to_use = mag_max

        # Plotting spectrogram.
        x_time, y_freq = np.meshgrid(time, freq)
        self.axes.clear()
        pcolor = self.axes.pcolormesh(x_time, np.fft.fftshift(y_freq), np.fft.fftshift(mag.T), vmin=mag_min_to_use, vmax=mag_max_to_use, cmap='coolwarm')
        self.axes.set_yscale('log')
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Frequency (Hz)')
        self.figure.colorbar(pcolor, label='Magnitud (dB)')
        if f_bottom is not None:
            self.axes.set_ylim(bottom=f_bottom)
        if f_top is not None:
            self.axes.set_ylim(top=f_top)

        self.axes.set_title(title)
        self.canvas.draw()