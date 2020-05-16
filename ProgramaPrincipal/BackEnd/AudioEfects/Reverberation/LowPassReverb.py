import numpy as np
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect


class LowPassReverb(Effect):
    default_properties = {"Absorción": ((float, (0, 1)), 0.3),
                  "Retardo (ms)": ((float, (0, 700)), 500)}

    def __init__(self, buffer_len: int = 2**15,  g: float = 0.3, delay: float = 500, sample_rate: int = 44100):
        super(LowPassReverb, self).__init__("Reverb low-pass")

        """ Buffer to keep old output """
        self.old_output = np.zeros(int(buffer_len))
        self.buffer_len = buffer_len
        self.sample_rate = sample_rate
        self.m = np.floor(delay * sample_rate / 1000.0)
        self.p2read = int(buffer_len - self.m)
        self.p2write = 0
        self.g = g/5.0

    def compute(self, sample: np.ndarray) -> np.ndarray:
        out = np.array([list(map(self.one_run, sample))])
        return (out, out)

    def one_run(self, sample):
        """ y(n) = x(n) - g (y(n-M) + y(n-M-1)  """
        out = sample - self.g * (self.old_output[self.p2read] + self.old_output[self.p2read - 1])

        """ keep old useful values """
        self.old_output[self.p2write] = out

        """ Circular buffer stuff """
        self.p2read += 1
        self.p2write += 1
        if self.p2read >= self.buffer_len:
            self.p2read = 0
        if self.p2write >= self.buffer_len:
            self.p2write = 0

        return out

    def get_impulse_response(self, buffer_length=44100) -> np.ndarray:
        delta = np.zeros(int(buffer_length))
        delta[0] = 1

        h = self.compute(delta)
        return h

    def clear(self):
        self.old_output = np.zeros(self.buffer_len)
        self.p2read = self.buffer_len - self.m
        self.p2write = 0

    def change_param(self, new_property, value):
        new_delay = 0
        new_gain = 0
        if new_property == "Absorción":
            new_gain = value
        elif new_property == "Retardo (ms)":
            new_delay = np.floor(value * self.sample_rate / 1000.0)

        self.g = new_gain/5.0
        self.m = new_delay if 0 < new_delay < self.buffer_len else new_delay % self.buffer_len  # Validate input
        p2w = self.p2write
        self.p2read = int(p2w - new_delay if p2w >= new_delay else p2w - new_delay + self.buffer_len)

