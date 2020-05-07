from numpy.fft import rfft
from scipy.signal import blackmanharris, fftconvolve
import numpy as np

def get_freq_from_fft(data, samprate):
    #Estimate frequency from peak of FFT   

    # Compute Fourier transform of windowed signal
    windowed = data * blackmanharris(len(data))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic_interpolation(np.log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return samprate * true_i / len(windowed)  

def parabolic_interpolation(input_vector, vector_index):
    '''
    Returns the coordinates of the vertex of a parabola that goes through point vector_index and
    its two neighbors.
    '''

    xv = 1/2. * (input_vector[vector_index-1] - input_vector[vector_index+1]) / (input_vector[vector_index-1] - 2 * input_vector[vector_index] + input_vector[vector_index+1]) + vector_index
    yv = input_vector[vector_index] - 1/4. * (input_vector[vector_index-1] - input_vector[vector_index+1]) * (xv - vector_index)
    return (xv, yv)