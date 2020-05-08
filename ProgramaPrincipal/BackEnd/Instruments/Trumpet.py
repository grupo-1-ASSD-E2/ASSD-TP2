from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
import numpy as np

from BackEnd.AdditiveSynthesis.PartialNote import PartialNote


class Trumpet:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.instrument_name = "Trumpet"

    def __get_partials__(self, frequency):
        freq_of_samples = 261.63

        multiplier = frequency / freq_of_samples
        

        partial1 = PartialNote(261.65532 * multiplier, 0.76483, 0.37, 0.627, 0.039, 0.89, 0.0297, 7.4, 0.028, 7.61)
        
        partial2 = PartialNote(523.310642 * multiplier, 0.1167782, 0.37, 0.487, 0.065, 0.627, 0.069, 7.4, 0.05, 7.60)

        partial3 = PartialNote(784.837889 * multiplier, -1.5167848, 0.37, 0.474, 0.0976, 0.627, 0.1175, 7.4, 0.084,
                               7.54)

        partial4 = PartialNote(1046.6212841 * multiplier, 1.4703592579, 0.37, 0.461, 0.117, 0.88, 0.167, 7.4, 0.1124,
                               7.51)

        partial5 = PartialNote(1308.2766 * multiplier, 1.646486, 0.37, 0.4486, 0.074, 0.716, 0.103, 7.4, 0.048, 7.51)

        partial6 = PartialNote(1569.803852 * multiplier, -0.554181, 0.37, 0.473, 0.13, 0.853, 0.162, 7.4, 0.094, 7.52)

        partial7 = PartialNote(1831.45917 * multiplier, -0.14542, 0.37, 0.46, 0.069, 0.815, 0.1026, 7.4, 0.0609, 7.5)

        partial8 = PartialNote(2093.8829 * multiplier, -2.553459, 0.37, 0.46, 0.052, 0.7645, 0.091, 7.4, 0.03686, 7.48)

        partial9 = PartialNote(2355.92248 * multiplier, 1.5498516, 0.37, 0.46, 0.034, 0.777, 0.0575, 7.4, 0.0271,
                               7.5)

        partial10 = PartialNote(2617.5778 * multiplier, -2.80477, 0.37, 0.4479, 0.037, 0.7645, 0.0684, 7.4, 0.0275, 7.5)

        partial11 = PartialNote(2879.7454 * multiplier, 2.781639, 0.37, 0.47, 0.045, 0.79, 0.075, 7.4, 0.0246, 7.5)

        partial12 = PartialNote(3141.4007 * multiplier, 1.441315, 0.37, 0.5, 0.0326, 0.82, 0.0488, 7.4, 0.012, 7.47)

        partial13 = PartialNote(3403.184136 * multiplier, -1.84469, 0.37, 0.449, 0.01259, 0.821, 0.03498, 7.4, 0.006485, 7.47)

        partial14 = PartialNote(3661.50953 * multiplier, 1.0291, 0.37, 0.462, 0.006575, 0.8213, 0.022, 7.4, 0.0051, 7.47)

        partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial7, partial8, partial9, partial10,
                    partial11, partial12, partial13, partial14]
        #partials = [partial1]
        return partials
