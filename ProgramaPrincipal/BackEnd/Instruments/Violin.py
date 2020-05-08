from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
import numpy as np

from BackEnd.AdditiveSynthesis.PartialNote import PartialNote


class Violin:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.instrument_name = "Violin"

    def __get_partials__(self, frequency):
        freq_of_samples = 261.63

        multiplier = frequency / freq_of_samples
        

       
        partial1 = PartialNote(261.58854 * multiplier, -2.93465, 0.47, 0.558, 0.16, 0.9566, 0.36457, 3.55, 0.3236, 3.942)

        partial2 = PartialNote(522.94078 * multiplier, 2.7098, 0.47, 0.558, 0.0365, 1, 0.16, 3.55, 0.153, 3.7)

        partial3 = PartialNote(784.52932 * multiplier, 0.363645, 0.47, 0.5173, 0.049, 1, 0.157, 3.55, 0.1317, 3.73)

        partial4 = PartialNote(1039.73765 * multiplier, 2.1862, 0.47, 0.5447, 0.0255, 0.86, 0.067, 3.55, 0.0429, 3.74)

        partial5 = PartialNote(1314.3229 * multiplier, 1.46007, 0.47, 0.517, 0.04, 0.98, 0.1, 3.55, 0.0575, 3.71)

        partial6 = PartialNote(1580.4012 * multiplier, 1.971578, 0.47, 0.724, 0.0245, 0.897, 0.0896, 3.55, 0.08, 3.74)

        partial7 = PartialNote(1841.98978 * multiplier, -0.59578, 0.47, 0.744, 0.0146, 1, 0.0472, 3.55, 0.0254, 3.7)

        partial8 = PartialNote(2091.054205 * multiplier, 3.101057, 0.47, 0.786, 0.00187, 0.99, 0.068, 3.55, 0.0432, 3.65)

        partial9 = PartialNote(2589.18306 * multiplier,0.03179217, 0.47, 0.856, 0.0347, 1.08, 0.079, 3.55, 0.0235, 3.7)

        partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial7, partial8, partial9]
        #partials = [partial1]
        return partials
