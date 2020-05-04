from ProgramaPrincipal.BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
import numpy as np


class Trumpet:
    def __init__(self):
        self.synthesizer = AdditiveSynthesizer()
        self.instrument_name = "Trumpet"

    def __get_partials__(self, frequency):
        c4_partial_freqs = [1.0039,
                            2.0087,
                            3.0143,
                            4.0182,
                            5.0257,
                            6.0296,
                            7.0299,
                            8.033,
                            9.0369,
                            10.0408,
                            11.0447,
                            12.0592
                            ]
        c4_partial_amplitudes = [0.1319,
                                 0.3897,
                                 0.6578,
                                 1,
                                 0.8518,
                                 0.6922,
                                 0.4748,
                                 0.3287,
                                 0.3369,
                                 0.2327,
                                 0.1634,
                                 0.1365
                                 ]

        out_freqs = np.asarray(c4_partial_freqs) * frequency
        c4_partial_amplitudes = np.asarray(c4_partial_amplitudes)
        return out_freqs, c4_partial_amplitudes
