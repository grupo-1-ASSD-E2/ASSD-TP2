from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
import numpy as np

from BackEnd.AdditiveSynthesis.PartialNote import PartialNote


class Oboe:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.instrument_name = "Oboe"

    def __get_partials__(self, frequency):
        freq_of_samples = 261.63

        multiplier = frequency / freq_of_samples
        

        partial1 = PartialNote(260.9281 * multiplier,-1.83709, 0, 0.1168, 0.132, 0.296, 0.128, 6.36, 0.124, 6.75)

        partial2 = PartialNote(521.712996 * multiplier,-1.43441, 0, 0.07, 0.07, 0.442, 0.07, 6.36, 0.07, 6.75)

        partial3 = PartialNote(782.641099 * multiplier,-1.3449376, 0, 0.139, 0.0987, 0.307, 0.0957, 6.36, 0.08, 6.77)

        partial4 = PartialNote(1043.13957 * multiplier,2.83307, 0, 0.15, 0.163, 0.35, 0.178, 6.36, 0.153, 6.78)

        partial5 = PartialNote(1304.0677 * multiplier,2.82392, 0, 0.117, 0.41, 0.42, 0.4, 6.36, 0.36, 6.7)

        partial6 = PartialNote(1564.85257 * multiplier,-2.6445677, 0, 0.103, 0.307, 0.24, 0.297, 6.36, 0.216, 6.7)

        partial7 = PartialNote(1825.92388 * multiplier,-1.5581, 0, 0.092, 0.2, 0.43, 0.2, 6.36, 0.185, 6.7)

        partial8 = PartialNote(2086.85198 * multiplier,-1.8931935, 0, 0.137, 0.0857, 0.375, 0.089, 6.36, 0.0688, 6.76)


        partial9 = PartialNote(2347.78 * multiplier,2.433, 0, 0.103, 0.013, 0.6, 0.019, 6.36, 0.019, 6.75)

        partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial7, partial8, partial9]
        #partials = [partial1]
        return partials