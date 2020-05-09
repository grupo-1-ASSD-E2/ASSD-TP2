import numpy as np
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class LowPassReverb(Effect):

    def __init__(self, buffer_len: int,  g: float, delay: float, sample_rate: int):
        super(LowPassReverb, self).__init__("Reverb low-pass")
        self.properties = {"Absorción": ((float, (0, 1)), g),
                           "Retardo (ms)": ((float, (0, buffer_len*1000.0/float(sample_rate))), delay)}

        """ Buffer to keep old output """
        self.old_output = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.sample_rate = sample_rate
        self.p2read = buffer_len - delay
        self.p2write = 0
        self.g = g
        self.m = np.floor(delay*sample_rate/1000.0)

    def compute(self, sample: np.ndarray, sample_size: int) -> np.ndarray:
        out = np.zeros(sample_size)
        for i in range(0, sample_size):
            in_value = sample[i]
            """ y(n) = x(n) + g (y(n-M) + y(n-M-1)  """
            out[i] = in_value + self.g * (self.old_output[self.p2read]+self.old_output[self.p2read-1])

            """ keep old useful values """
            self.old_output[self.p2write] = out[i]

            """ Circular buffer stuff """
            self.p2read += 1
            self.p2write += 1
            if self.p2read >= self.buffer_len:
                self.p2read = 0
            if self.p2write >= self.buffer_len:
                self.p2write = 0
        return out.copy()

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1

        h = self.compute(delta, buffer_length)
        return h

    def reset(self):
        self.old_output = np.zeros(self.buffer_len)
        self.p2read = self.buffer_len - self.m
        self.p2write = 0

    def change_param(self, new_properties):
        new_gain = new_properties["Absorción"][1]
        new_delay = np.floor(new_properties["Retardo (ms)"][1] * self.sample_rate / 1000.0)

        self.g = new_gain if new_gain > 1 else self.g  # Validate input
        self.m = new_delay if 0 < new_delay < self.buffer_len else new_delay % self.buffer_len  # Validate input
        p2w = self.p2write
        self.p2read = p2w - new_delay if p2w >= new_delay else p2w - new_delay + self.buffer_len

