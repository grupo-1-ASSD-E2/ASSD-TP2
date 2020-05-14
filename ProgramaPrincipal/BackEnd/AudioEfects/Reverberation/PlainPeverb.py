import numpy as np
from BackEnd.AudioEfects.Filters.Comb import CombFilter
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class PlainReverb(Effect):
    default_properties = {"Tiempo de Reverberacion (s)": ((float, (0.1, 10)), 1),
                           "Delay (ms)": ((float, (0, 700)), 300)}

    def __init__(self, buffer_len: int = 2**15, sample_rate: int = 44100, t_60=1):
        super(PlainReverb, self).__init__("Reverb plain")

        self.defaults_N = 15323
        self.sample_rate = sample_rate
        self.g = 10**(-3*self.defaults_N/(sample_rate*t_60))
        self.buffer_len = buffer_len
        self.c1 = CombFilter(buffer_len, self.g, self.defaults_N)

    def compute(self, audio_input: np.ndarray):
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

    def change_param(self, new_property, value):
        new_t_60 = 0
        new_delay = 0
        if new_property == "Tiempo de Reverberacion (s)":
            new_t_60 = value
        elif new_property == "Delay (ms)":
            new_delay = value
        n = np.floor(new_delay * self.sample_rate / 1000.0)
        n = n if n != self.defaults_N else None
        self.change_t_60(new_t_60, n)

    def change_t_60(self, new_t_60: float, new_n: int = None):
        self.defaults_N = new_n if new_n is not None else self.defaults_N
        self.g = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.g, self.defaults_N)
