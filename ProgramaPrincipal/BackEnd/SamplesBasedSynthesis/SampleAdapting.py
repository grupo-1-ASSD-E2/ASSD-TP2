import os
import numpy as np
import soundfile as sf 
import sys


def note_scaling(input_data, input_samp, shift):
	'''
	This function initiates the call to start shifting the pitch by the factor shift.
	Returns: pitched sound as array
	'''

	transposed = pitch_shift(input_data, shift)
	return transposed.astype(input_data.dtype)

def pitch_shift(input_data, n, DFT_size = 2**11, hop_size=2048/8):
	'''
	This function begins to change the pitch of the sound by implementing the Phase Vocoder method. 
	That is first time-stretching the sound, then speedh changing it all by a common factor.
	'''
	#changes the pitch of a sound by n semitones
	factor = 2**(1.0 * n / 12.0)
	stretched = time_stretch(input_data, 1.0/factor, DFT_size, hop_size)
	return change_speed(stretched[DFT_size:], factor)

def change_speed(input_data, factor): 
	'''
	This function changes the speed of playback of the .WAV file by some factor. It is used with pitching to accomodate the speed.
	'''

	indices = np.round(np.arange(0, len(input_data), factor)) #Create an even-spaced array (input_data) spaced by the factor.
	indices = indices[indices < len(input_data)].astype(int) #Astype int takes the neghboring values to these, but then preserves the same vector length. 
	return input_data[indices.astype(int)]

def time_stretch(input_data, factor, DFT_size=2**11, hop_size=2**11/8):
	'''
	This function stretches the input file by an input factor maintaining its pitch.
	Returns: Array of the note shifted by factor.
	'''
	
	L = len(input_data)
	#set up our signal arrays to hold the processing output
	phi = np.zeros(DFT_size) #create an array of zeros (float) of DFT_size
	out = np.zeros(DFT_size, dtype = complex)
	signal_out = np.zeros(int(round(L/factor)) + DFT_size, dtype = complex)

	#Find out what the peak amplitude of input is (for scaling) and create a hanning window
	amp = max(input_data)
	hanning_window = np.hanning(DFT_size)

	p = 0
	pp = 0
	while p < L - (DFT_size + hop_size):

		#take the spectra of two consecutive windows
		p1 = int(p)
		spectra_1 = np.fft.fft(hanning_window * input_data[p1: p1 + int(DFT_size)])
		spectra_2 = np.fft.fft(hanning_window * input_data[p1 + int(hop_size): p1 + int(DFT_size) + int(hop_size)])

		#take their phase difference and integrate
		phi += (np.angle(spectra_2) - np.angle(spectra_1)) #about aligning two nieghboring spectra, by looking at the relative shifts of phase at each frequency bin - based on their phase difference 
		#determine how to line them up without any discontinuities at the boundaries.

		#bring the phase back between pi and -pi
		for i in phi:
			while i < -np.pi: i += 2*np.pi
			while i >= np.pi: i -= 2*np.pi

		out.real, out.imag = np.cos(phi), np.sin(phi)
		#inverse FFT and overlap-add to reconstruct the sequence
		signal_out[pp:pp+int(DFT_size)] += (hanning_window * np.fft.ifft(np.abs(spectra_2)*out)) 
		pp += int(hop_size)
		p += hop_size*factor

	#write the output and scale it to match the original amplitude
	signal_out = amp*signal_out/max(signal_out)

	return signal_out.astype(input_data.dtype)

def phase_vocoder(D, rate, hop_length=None):
    """
    Parameters
    ----------
    D : np.ndarray [shape=(d, t), dtype=complex]
        STFT matrix

    rate :  float > 0 [scalar]
        Speed-up factor: `rate > 1` is faster, `rate < 1` is slower.

    hop_length : int > 0 [scalar] or None
        The number of samples between successive columns of `D`.

        If None, defaults to `n_fft/4 = (D.shape[0]-1)/2`

    Returns
    -------
    D_stretched : np.ndarray [shape=(d, t / rate), dtype=complex]
        time-stretched STFT

    """

    n_fft = 2 * (D.shape[0] - 1)

    if hop_length is None:
        hop_length = int(n_fft // 4)

    time_steps = np.arange(0, D.shape[1], rate, dtype=np.float)

    # Create an empty output array
    d_stretch = np.zeros((D.shape[0], len(time_steps)), D.dtype, order='F')

    # Expected phase advance in each bin
    phi_advance = np.linspace(0, np.pi * hop_length, D.shape[0])

    # Phase accumulator; initialize to the first sample
    phase_acc = np.angle(D[:, 0])

    # Pad 0 columns to simplify boundary logic
    D = np.pad(D, [(0, 0), (0, 2)], mode='constant')

    for (t, step) in enumerate(time_steps):

        columns = D[:, int(step):int(step + 2)]

        # Weighting for linear magnitude interpolation
        alpha = np.mod(step, 1.0)
        mag = ((1.0 - alpha) * np.abs(columns[:, 0])
               + alpha * np.abs(columns[:, 1]))

        # Store to output array
        d_stretch[:, t] = mag * np.exp(1.j * phase_acc)

        # Compute phase advance
        dphase = (np.angle(columns[:, 1])
                  - np.angle(columns[:, 0])
                  - phi_advance)

        # Wrap to -pi:pi range
        dphase = dphase - 2.0 * np.pi * np.round(dphase / (2.0 * np.pi))

        # Accumulate phase
        phase_acc += phi_advance + dphase

    return d_stretch