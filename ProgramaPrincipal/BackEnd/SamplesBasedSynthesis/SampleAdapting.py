import os
import numpy as np
import soundfile as sf 
import sys
import librosa

def note_scaling(input_data, input_samp, shift, time_factor):
	'''
	This function initiates the call to start shifting the pitch by the parameter shift.
	Returns: pitched sound as array
	'''
	transposed = pitch_shift(input_data, shift, time_factor)
	return transposed.astype(input_data.dtype)

def pitch_shift(input_data, n, time_factor, DFT_size = 2**11, hop_size=2048//4):
	'''
	This function begins to change the pitch of the sound by implementing the Phase Vocoder method. 
	That is first time-stretching the sound, then speedh changing it all by a common factor.
	'''
	#changes the pitch of a sound by n semitones
	factor = 2**(1.0 * n / 12.0)
	#stretched = time_stretch(input_data, 1.0/factor, DFT_size, hop_size)
	stretched = stretch(input_data, len(input_data) / (len(input_data) * factor + DFT_size)*time_factor)
	return change_speed(stretched[DFT_size:], factor)

def change_speed(input_data, factor): 
	'''
	This function changes the speed of playback of the .WAV file by some factor. It is used with pitching to accomodate the speed.
	'''
	indices = np.round(np.arange(0, len(input_data), factor)) #Create an even-spaced array (input_data) spaced by the factor.
	indices = indices[indices < len(input_data)].astype(int) #Astype int takes the neghboring values to these, but then preserves the same vector length. 
	return input_data[indices.astype(int)]

def stretch(x, factor, nfft=2048):
    '''
    Stretch x by a factor
    '''
    stft = librosa.core.stft(x, n_fft=nfft).transpose()
    stft_rows = stft.shape[0]
    stft_cols = stft.shape[1]

    times = np.arange(0, stft.shape[0], factor)  # times at which new FFT to be calculated
    hop = nfft/4                                 # frame shift
    stft_new = np.zeros((len(times), stft_cols), dtype=np.complex_)
    phase_adv = (2 * np.pi * hop * np.arange(0, stft_cols))/ nfft
    phase = np.angle(stft[0])
    
    stft = np.concatenate( (stft, np.zeros((1, stft_cols))), axis=0)

    for i, time in enumerate(times):
        left_frame = int(np.floor(time))
        local_frames = stft[[left_frame, left_frame + 1], :]
        right_wt = time - np.floor(time)                    
        local_mag = (1 - right_wt) * np.absolute(local_frames[0, :]) + right_wt * np.absolute(local_frames[1, :])
        local_dphi = np.angle(local_frames[1, :]) - np.angle(local_frames[0, :]) - phase_adv
        local_dphi = local_dphi - 2 * np.pi * np.floor(local_dphi/(2 * np.pi))
        stft_new[i, :] =  local_mag * np.exp(phase*1j)
        phase += local_dphi + phase_adv

    return librosa.core.istft(stft_new.transpose())