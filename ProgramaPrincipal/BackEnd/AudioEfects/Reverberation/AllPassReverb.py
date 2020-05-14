import numpy as np
from BackEnd.AudioEfects.Filters.AllPass import AllPassFilter
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class AllPassReverb(Effect):
    default_properties = {"Tiempo de Reverberacion (s)": ((float, (0, 10)), 1),
                  "Delay (ms)": ((float, (0, 700)), 44.8)}

    def __init__(self, buffer_len=2**15, sample_rate: int = 44100, t_60=1):
        super(AllPassReverb, self).__init__("Reverb all-pass")

        self.sample_rate = sample_rate
        self.defaults_N = 1979
        self.g = 10 ** (-3 * self.defaults_N / (sample_rate * t_60))  # review
        self.buffer_len = buffer_len
        self.c1 = AllPassFilter(buffer_len, self.g, self.defaults_N)

    def compute(self, audio_input: np.ndarray):
        audio_input = audio_input[0]
        out = self.c1.compute(audio_input)
        out = np.array([out])
        output = (out.copy(), out.copy())
        return output

    def get_impulse_response(self) -> np.ndarray:
        delta = np.zeros(int(self.buffer_len))
        delta[0] = 1
        h = self.c1.compute(delta)

        return h

    def clear(self):
        self.c1.reset()

    def change_param(self, new_property, value):
        new_t_60 = 0
        n = 0
        if new_property == "Tiempo de Reverberacion (s)":
            new_t_60 = value
        elif new_property == "Delay (ms)":
            new_delay = value
            n = int(np.floor(new_delay * self.sample_rate / 1000.0))
            n = n if n != self.defaults_N else None

        self.change_t_60(new_t_60, n)

    def change_t_60(self, new_t_60: float, new_n=None):
        self.defaults_N = new_n if new_n is not None else self.defaults_N
        self.g = 10 ** (-3 * self.defaults_N / (44100 * new_t_60))
        self.c1.change_param(self.g, self.defaults_N)

