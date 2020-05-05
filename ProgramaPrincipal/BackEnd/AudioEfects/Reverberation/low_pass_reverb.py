import numpy as np


class LowPassReverb(object):

    def __init__(self, buffer_len: int,  a: float, delay: int):
        """ Buffer to keep old output """
        self.old_output = np.zeros(int(buffer_len))
        self.old_input = 0
        self.buffer_len = buffer_len
        self.p2read = buffer_len - delay
        self.p2write = 0
        self.a = a
        self.m = delay

    def compute(self, sample: np.ndarray, sample_size: int) -> np.ndarray:
        out = np.zeros(sample_size)
        for i in range(0, sample_size):
            in_value = sample[i]
            """ y(n) = x(n) + (x(n)+x(n-1))/A * y(n-M) / Comb filter equation """
            out[i] = in_value + ((in_value + self.old_input)/self.a) * self.old_output[self.p2read]

            """ keep old useful values """
            self.old_output[self.p2write] = out[i]
            self.old_input = in_value

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
        self.old_input = 0

    def change_param(self, new_gain, new_delay):
        self.a = new_gain if new_gain > 1 else self.a  # Validate input
        self.m = new_delay if 0 < new_delay < self.buffer_len else self.m  # Validate input
        p2w = self.p2write
        self.p2read = p2w - new_delay if p2w >= new_delay else p2w - new_delay + self.buffer_len
