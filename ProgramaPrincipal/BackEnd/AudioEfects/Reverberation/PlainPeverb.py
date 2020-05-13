import numpy as np
from BackEnd.AudioEfects.Filters.Comb import CombFilter
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class PlainReverb(Effect):

    def __init__(self, buffer_len: int = 2**15, sample_rate: int = 44100, t_60=1):
        super(PlainReverb, self).__init__("Reverb plain")
        self.properties = {"Tiempo de Reverberacion (s)": ((float, (0, 10)), t_60),
                           "Delay (ms)": ((float, (0, buffer_len * 1000.0 / float(sample_rate))),
                                          1979 / (float(sample_rate) * 1000))}

        self.defaults_N = 15323
        self.sample_rate = sample_rate
        self.g = 10**(-3*self.defaults_N/(sample_rate*t_60))
        self.buffer_len = buffer_len
        self.c1 = CombFilter(buffer_len, self.g, self.defaults_N)

    def compute(self, audio_input: np.ndarray):
        audio_input = audio_input[0]
        out = self.c1.compute(audio_input)
        out = np.array([out])
        output = (out, out)
        return output

    def clear(self):
        self.c1.reset()

    def get_impulse_response(self) -> np.ndarray:
        delta = np.zeros(int(self.buffer_len))
        delta[0] = 1
        h = self.c1.compute(delta)

        return h

    def change_param(self, new_properties):
        new_t_60 = new_properties["Tiempo de Reverberacion (s)"][1]
        new_delay = new_properties["Delay (ms)"][1]
        n = np.floor(new_delay * 1000 * self.sample_rate)
        n = n if n != self.defaults_N else None
        self.change_t_60(new_t_60, n)

    def change_t_60(self, new_t_60: float, new_n=None):
        self.defaults_N = new_n if new_n is not None else self.defaults_N
        self.g = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.g, self.defaults_N)
