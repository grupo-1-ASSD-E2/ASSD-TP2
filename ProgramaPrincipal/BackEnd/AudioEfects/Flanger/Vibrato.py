import numpy as np
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class Vibrato(Effect):

    def __init__(self, buffer_len, sample_rate, gain=0.7, delay=1, f0=5):
        super(Vibrato, self).__init__("Eco")
        self.properties = {"Retraso (ms)": ((float, (0, 5)), delay),
                           "Frecuecia (Hz)": ((float, (0, 100)), f0),
                           "Profundidad": ((float, (0, 1)), gain)}

        self.fo = f0
        self.sample_rate = sample_rate
        self.old_input = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.g = gain
        self.a = 0.5
        self.m0 = np.floor(sample_rate*delay/((1-self.a)*1000))
        self.p2read = buffer_len - self.m0
        self.p2write = 0

    def compute(self, sample: np.ndarray) -> np.ndarray:
        out = np.zeros(self.buffer_len)
        """ To increase efficiency """
        k = 2*np.pi*self.fo/self.sample_rate
        sin = np.sin
        m0 = self.m0
        a = self.a
        g = self.g

        for i in range(0, self.buffer_len):
            """ y(n) = g x(n) + (1-g) x(n-M(n))  """
            p2read_b = np.floor(self.p2read + m0*sin(k*i))
            p2read_b = p2read_b % self.buffer_len if p2read_b >= self.buffer_len else p2read_b

            out[i] = (1-g)*sample[i] + g * self.old_input[int(p2read_b)]

            """ keep old output values """
            self.old_input[self.p2write] = sample[i]

            """ Circular buffer stuff """
            self.p2read += 1
            self.p2write += 1
            if self.p2read >= self.buffer_len:
                self.p2read = 0
            if self.p2write >= self.buffer_len:
                self.p2write = 0

        output = (out, out)
        return output

    def change_param(self, new_properties):
        self.fo = new_properties["Frecuecia (Hz)"][1]
        self.g = new_properties["Profundidad"][1]
        delay = new_properties["Retraso (ms)"][1]/1000
        self.m0 = np.floor(self.sample_rate * delay / (1 - self.a))


