import numpy as np
from BackEnd.AudioEfects.Filters.AllPass import AllPassFilter
from BackEnd.AudioEfects.Filters.Comb import CombFilter
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class Reverb(Effect):
    default_properties = {"Tiempo de Reverberacion (s)": ((float, (0, 10)), 2)}

    def __init__(self, buffer_len: int = 2**15,  sample_rate: int = 44100, t_60=3):
        super(Reverb, self).__init__("Reverb")

        self.defaults_N = np.array([1373, 1583, 1783, 1979])
        self.defaults_N_2 = np.array([73, 21])
        self.gi = 10**(-3*self.defaults_N/(44100*t_60))
        self.gj = 10**(-3*self.defaults_N_2/(44100*t_60))
        self.sample_rate = sample_rate
        self.buffer_len = buffer_len

        self.c1 = CombFilter(buffer_len, self.gi[0], self.defaults_N[0])
        self.c2 = CombFilter(buffer_len, self.gi[1], self.defaults_N[1])
        self.c3 = CombFilter(buffer_len, self.gi[2], self.defaults_N[2])
        self.c4 = CombFilter(buffer_len, self.gi[3], self.defaults_N[3])
        self.a1 = AllPassFilter(buffer_len, self.gj[0], self.defaults_N_2[0])
        self.a2 = AllPassFilter(buffer_len, self.gj[1], self.defaults_N_2[1])

    def compute(self, audio_input: np.ndarray):

        audio_input = audio_input[0]
        y_a = (self.c1.compute(audio_input) + self.c2.compute(audio_input) + self.c3.compute(audio_input) +
               self.c4.compute(audio_input)) / 4
        out = self.a1.compute(self.a2.compute(y_a))

        out = np.array([out])
        output = (out, out)
        return output

    def get_impulse_response(self) -> np.ndarray:
        delta = np.zeros(int(self.buffer_len))
        delta[0] = 1
        ya = (self.c1.compute(delta) + self.c2.compute(delta) +
              self.c3.compute(delta) + self.c4.compute(delta))/4
        h = self.a1.compute(self.a2.compute(ya))

        return h

    def clear(self):
        self.c1.reset()
        self.c2.reset()
        self.c3.reset()
        self.c4.reset()
        self.c1.reset()
        self.a2.reset()

    def change_param(self, new_property, value):
        new_t_60 = 0
        if new_property == "Tiempo de Reverberacion (s)":
            new_t_60 = value

        self.change_t_60(new_t_60)

    def change_t_60(self, new_t_60: float):
        self.gi = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.gi[0], self.defaults_N[0])
        self.c2.change_param(self.gi[1], self.defaults_N[1])
        self.c3.change_param(self.gi[2], self.defaults_N[2])
        self.c4.change_param(self.gi[3], self.defaults_N[3])

