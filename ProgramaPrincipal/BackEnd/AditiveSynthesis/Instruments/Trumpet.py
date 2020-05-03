from ProgramaPrincipal.BackEnd.AditiveSynthesis.Instruments.Instrument import Instrument
import numpy as np


class Trumpet(Instrument):

    def __init__(self):
        i = 0

    def create_note_sig(self, note):
        first_zero_values, middle_values, last_zero_values = np.split(note.time_array,
                                                                      (note.note_on_index, note.note_off_index))

        first_zero_values = [0] * len(first_zero_values)

        last_zero_values = [0] * len(last_zero_values)

        frequencies, amplitudes = self.__get_partials__(note.frequency)

        middle_time_values = middle_values.copy()

        for i in range (0, len(frequencies)):
            if i == 0:
                middle_values = amplitudes[i] * np.sin(frequencies[i] * 2 * np.pi * (middle_time_values - note.note_on_time))
            else:
                middle_values += amplitudes[i] * np.sin(frequencies[i] * 2 * np.pi * (middle_time_values - note.note_on_time))

        #middle_values = np.sin(note.frequency * 2 * np.pi * (middle_values - note.note_on_time))

        signal = np.concatenate([first_zero_values, middle_values, last_zero_values])

        note.y_values = signal

    def __get_partials__(self, frequency):
        c4_freq = 261.63
        c4_partial_freqs = [0.994,
                            1.987,
                            2.989,
                            3.991,
                            4.993,
                            5.961,
                            6.988,
                            7.94,
                            ]
        c4_partial_amplitudes=[0.812,
                                1,
                                0.882,
                                0.587,
                                0.364,
                                0.295,
                                0.186,
                                0.126,
                                ]

        out_freqs = np.asarray(c4_partial_freqs) * frequency
        c4_partial_amplitudes = np.asarray(c4_partial_amplitudes)
        return out_freqs, c4_partial_amplitudes




    def __add_adsr__(self):
        raise NotImplementedError('setup adsr not implemented')

    def setup_adsr(self):
        raise NotImplementedError('setup adsr not implemented')
