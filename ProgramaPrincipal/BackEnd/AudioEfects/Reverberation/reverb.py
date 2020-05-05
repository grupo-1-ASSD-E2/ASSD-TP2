import numpy as np
from filters.all_pass import AllPassFilter
from filters.comb import CombFilter


class Reverb(object):

    def __init__(self, sample_rate: int, t_60=1):
        self.defaults_N = np.array([1373, 1583, 1783, 1979])
        self.gi = 10**(-3*self.defaults_N/(44100*t_60))

        self.c1 = CombFilter(sample_rate, self.gi[0], self.defaults_N[0])
        self.c2 = CombFilter(sample_rate, self.gi[1], self.defaults_N[1])
        self.c3 = CombFilter(sample_rate, self.gi[2], self.defaults_N[2])
        self.c4 = CombFilter(sample_rate, self.gi[3], self.defaults_N[3])
        self.a1 = AllPassFilter(sample_rate, 0.7, 1400)
        self.a2 = AllPassFilter(sample_rate, 0.7, 2000)

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1
        ya = (self.c1.compute(delta, buffer_length) + self.c2.compute(delta, buffer_length) +
              self.c3.compute(delta, buffer_length) + self.c4.compute(delta, buffer_length))/4
        h = self.a1.compute(self.a2.compute(ya, buffer_length), buffer_length)

        return h

    def change_t_60(self, new_t_60: float):
        self.gi = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.gi[0], self.defaults_N[0])
        self.c2.change_param(self.gi[1], self.defaults_N[1])
        self.c3.change_param(self.gi[2], self.defaults_N[2])
        self.c4.change_param(self.gi[3], self.defaults_N[3])

    def __get_filters_response_debug__(self):
        h1 = self.c1.get_impulse_response()
        h2 = self.c2.get_impulse_response()
        h3 = self.c3.get_impulse_response()
        h4 = self.c4.get_impulse_response()
        h5 = self.a1.get_impulse_response()
        h6 = self.a2.get_impulse_response()

        return h1, h2, h3, h4, h5, h6
