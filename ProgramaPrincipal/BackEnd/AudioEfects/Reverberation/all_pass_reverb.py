import numpy as np
from filters.all_pass import AllPassFilter


class AllPassReverb(object):

    def __init__(self, sample_rate: int, t_60=1):
        self.defaults_N = 1979
        self.g = 10 ** (-3 * self.defaults_N / (sample_rate * t_60))  # review

        self.c1 = AllPassFilter(sample_rate, self.g, self.defaults_N)

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1
        h = self.c1.compute(delta, buffer_length)

        return h

    def change_t_60(self, new_t_60: float, new_n=None):
        self.defaults_N = new_n if new_n is not None else self.defaults_N
        self.g = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.g, self.defaults_N)

