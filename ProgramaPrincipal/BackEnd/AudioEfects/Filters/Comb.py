import numpy as np


class CombFilter(object):

    def __init__(self, buffer_len, gain, delay):
        """ Buffer to keep old output """
        self.old_output = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.p2read = buffer_len-delay
        self.p2write = 0
        self.g = gain
        self.m = delay

    def compute(self, sample: np.ndarray, sample_size: int) -> np.ndarray:
        out = np.zeros(sample_size)
        for i in range(0, sample_size):
            """ y(n) = x(n) + g y(n-M) / Comb filter equation """
            out[i] = sample[i] + self.g * self.old_output[self.p2read]

            """ keep old output values """
            self.old_output[self.p2write] = out[i]

            """ Circular buffer stuff """
            self.p2read += 1
            self.p2write += 1
            if self.p2read >= self.buffer_len:
                self.p2read = 0
            if self.p2write >= self.buffer_len:
                self.p2write = 0
        return out.copy()

    def reset(self):
        self.old_output = np.zeros(self.buffer_len)
        self.p2read = self.buffer_len - self.m
        self.p2write = 0

    def change_param(self, new_gain, new_delay):
        self.g = new_gain
        self.m = new_delay
        p2w = self.p2write
        self.p2read = p2w - new_delay if p2w >= new_delay else p2w - new_delay + self.buffer_len

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1

        h = self.compute(delta, buffer_length)
        return h
