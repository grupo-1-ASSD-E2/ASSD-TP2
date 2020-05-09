import numpy as np
from BackEnd.AudioEfects.Filters.AllPass import AllPassFilter
from BackEnd.AudioEfects.Filters.Comb import CombFilter
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class Reverb(Effect):

    def __init__(self, buffer_len: int,  sample_rate: int = 44100, t_60=1):
        super(Reverb, self).__init__("Reverb")
        self.properties = {"Tiempo de Reverberacion (s)": ((float, (0, 10)), t_60)}

        self.defaults_N = np.array([1373, 1583, 1783, 1979])
        self.gi = 10**(-3*self.defaults_N/(44100*t_60))
        self.sample_rate = sample_rate
        self.buffer_len = buffer_len

        self.c1 = CombFilter(buffer_len, self.gi[0], self.defaults_N[0])
        self.c2 = CombFilter(buffer_len, self.gi[1], self.defaults_N[1])
        self.c3 = CombFilter(buffer_len, self.gi[2], self.defaults_N[2])
        self.c4 = CombFilter(buffer_len, self.gi[3], self.defaults_N[3])
        self.a1 = AllPassFilter(buffer_len, 0.7, 1400)
        self.a2 = AllPassFilter(buffer_len, 0.7, 2000)

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1
        ya = (self.c1.compute(delta, buffer_length) + self.c2.compute(delta, buffer_length) +
              self.c3.compute(delta, buffer_length) + self.c4.compute(delta, buffer_length))/4
        h = self.a1.compute(self.a2.compute(ya, buffer_length), buffer_length)

        return h

    def change_param(self, new_properties):
        new_t_60 = new_properties["Tiempo de Reverberacion (s)"][1]
        self.change_t_60(new_t_60)

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
