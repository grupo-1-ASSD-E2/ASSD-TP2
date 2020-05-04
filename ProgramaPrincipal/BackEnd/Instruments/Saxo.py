from ProgramaPrincipal.BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
import numpy as np


class Saxo:
    def __init__(self):
        self.synthesizer = AdditiveSynthesizer()
        self.instrument_name = 'Saxo'

    def __get_partials__(self, frequency):
        c4_partial_freqs = [1.0035,
                            2.008,
                            3.0146,
                            4.0192,
                            6.0189,
                            7.0328,
                            10.0328,
                            11.0561,

                            ]
        c4_partial_amplitudes = [1,
                                 0.593,
                                 0.4812,
                                 0.2462,
                                 0.1111,
                                 0.0688,
                                 0.0505,
                                 0.0643,

                                 ]

        out_freqs = np.asarray(c4_partial_freqs) * frequency
        c4_partial_amplitudes = np.asarray(c4_partial_amplitudes)
        return out_freqs, c4_partial_amplitudes
