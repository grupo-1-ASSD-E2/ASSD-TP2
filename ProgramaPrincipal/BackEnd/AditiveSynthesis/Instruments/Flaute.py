from ProgramaPrincipal.BackEnd.AditiveSynthesis.Instruments.Instrument import Instrument
import numpy as np


class Flaute(Instrument):

    def __init__(self):
        i = 0

    def create_note_sig(self, note):

        first_zero_values, middle_values, last_zero_values = np.split(note.time_array,(note.note_on_index, note.note_off_index))

        first_zero_values = [0] * len(first_zero_values)

        last_zero_values = [0] *  len(last_zero_values)

        middle_values = np.sin(note.frequency * 2 * np.pi * (middle_values - note.note_on_time))

        signal = np.concatenate([first_zero_values, middle_values, last_zero_values])

        note.y_values = signal

    def __add_adsr__(self):
        raise NotImplementedError('add adsr not implemented')

    def setup_adsr(self):
        raise NotImplementedError('setup adsr not implemented')
