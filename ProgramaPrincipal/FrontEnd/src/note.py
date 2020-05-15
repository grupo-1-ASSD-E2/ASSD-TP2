import numpy as np

class note:
    def __init__(self, init_time=0, duration=0, velocity=0, instrument='', note_freq=0):
        self.init_time = init_time
        self.duration = duration + init_time
        self.velocity = velocity
        self.instrument = instrument #recordar que los instrumentos empiezan con mayusc
        self.note_number = self.__freq_to_note__(note_freq)
        self.fs=44100

    @staticmethod
    def __freq_to_note__(freq):
        a = 440  # frequency of A (coomon value is 440Hz)
        return int(round(np.log2(freq * ( 32 / a)) * 12 + 9))
        