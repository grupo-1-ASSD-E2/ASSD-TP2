from ProgramaPrincipal.BackEnd.AditiveSynthesis.Instruments.Instrument import Instrument

import numpy as np


class Note:

    @staticmethod
    def __midi_note_to_frequency__(midi_note_code):
        a = 440  # frequency of A (common value is 440Hz)
        return (a / 32) * (2 ** ((midi_note_code - 9) / 12))

    def __init__(self, time_array, midi_number, note_on_time):
        self.midi_note_number = midi_number
        self.frequency = self.__midi_note_to_frequency__(midi_number)

        self.instrument_assigned = None
        self.time_array = time_array
        self.y_values = []

        self.note_on_time = note_on_time  # in seconds
        self.note_off_time = -1  # in seconds
        self.note_on_index = np.where(np.isclose(self.time_array, self.note_on_time))[0][0]  #

        self.note_off_index = None
        self.has_note_off_time = False

        self.volume = 1

    def note_off(self, note_off_time):
        self.note_off_time = note_off_time
        self.note_off_index = np.where(np.isclose(self.time_array, self.note_off_time))[0][0]  #
        self.has_note_off_time = True
        self.create_note_signal()

    def create_note_signal(self):
        if self.instrument_assigned is not None:
            self.instrument_assigned.create_note_sig(self)

    def assing_instrument(self, instrument):
        self.instrument_assigned = instrument
