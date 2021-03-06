import numpy as np
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class EcoSimple(Effect):

    default_properties = {"Absorción": ((float, (0, 1)), 0.7),
                  "Retardo (ms)": ((float, (0, 700)), 20)}

    def __init__(self, buffer_len=2**15, gain=0.7, delay=20, sample_rate=44100):
        super(EcoSimple, self).__init__("Eco")
        self.properties = {"Absorción": gain, "Retardo (ms)": delay}

        self.old_input = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.sample_rate = sample_rate
        self.m = np.floor(delay * sample_rate / 1000.0)
        self.p2read = int(buffer_len - self.m)
        self.p2write = 0
        self.g = gain

    def compute(self, sample: np.ndarray) -> np.ndarray:
        out = np.array([list(map(self.one_run, sample))])

        return (out, out)

    def one_run(self, sample):
        """ y(n) = x(n) + g x(n-M) / Comb filter equation """
        out = sample + self.g * self.old_input[self.p2read]
        """ keep old output values """
        self.old_input[self.p2write] = sample

        """ Circular buffer stuff """
        self.p2read += 1
        self.p2write += 1
        if self.p2read >= self.buffer_len:
            self.p2read = 0
        if self.p2write >= self.buffer_len:
            self.p2write = 0

        return out

    def clear(self):
        self.old_input = np.zeros(int(self.buffer_len))
        self.p2read = int(self.buffer_len - self.m)
        self.p2write = 0

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1
        h = self.compute(delta)

        return h

    def change_param(self, new_property, value):
        new_gain = 0
        new_delay = 0
        if new_property == "Absorción":
            new_gain = value
        elif new_property == "Retardo (ms)":
            new_delay = np.floor(value*self.sample_rate/1000.0)

        self.g = new_gain if new_gain > 1 else self.g  # Validate input
        self.m = new_delay if 0 < new_delay < self.buffer_len else new_delay % self.buffer_len  # Validate input
        p2w = self.p2write
        self.p2read = int(p2w - new_delay if p2w >= new_delay else p2w - new_delay + self.buffer_len)

