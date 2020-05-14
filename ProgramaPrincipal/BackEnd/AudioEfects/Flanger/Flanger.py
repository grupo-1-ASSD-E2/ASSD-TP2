import numpy as np
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class Flanger(Effect):
    default_properties = {"Retraso (ms)": ((float, (0, 5)), 1),
                  "Frecuecia (Hz)": ((float, (0, 100)), 5)}

    def __init__(self, buffer_len=2**15, sample_rate=44100, delay=1, f0=5):
        super(Flanger, self).__init__("Flanger")

        self.fo = f0
        self.sample_rate = sample_rate
        self.old_input = np.zeros(int(buffer_len))
        self.old_output = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.g = 1/3.0
        self.m0 = np.floor(sample_rate*delay/1000)
        self.p2read = buffer_len - self.m0
        self.p2write = 0

    def compute(self, sample: np.ndarray) -> np.ndarray:
        sample = sample[0]
        """ To increase efficiency """
        k = 2*np.pi*self.fo/self.sample_rate
        sin = np.sin
        m0 = self.m0
        g = [self.g]*self.buffer_len
        offset = [m0 * sin(k * i) for i in range(0, self.buffer_len)]

        out = np.array([list(map(self.one_run, sample, offset, g))])
        output = (out, out)
        return output

    def one_run(self, sample, offset, g):
        p2read_b = np.floor(self.p2read + offset)
        p2read_b = int(p2read_b % self.buffer_len if p2read_b >= self.buffer_len else p2read_b )

        """ y(n) = g ( x(n) + x(n-M(n) + y(n-M(n) )  """
        out = g * (sample + self.old_input[p2read_b] + self.old_output[p2read_b])

        """ keep old output values """
        self.old_input[self.p2write] = sample
        self.old_output[self.p2write] = out

        """ Circular buffer stuff """
        self.p2read += 1
        self.p2write += 1
        if self.p2read >= self.buffer_len:
            self.p2read = 0
        if self.p2write >= self.buffer_len:
            self.p2write = 0

        return out

    def change_param(self, new_property, value):
        if new_property == "Frecuecia (Hz)":
            self.fo = value
        elif new_property == "Retraso (ms)":
            delay = value/1000
            self.m0 = np.floor(self.sample_rate * delay)


