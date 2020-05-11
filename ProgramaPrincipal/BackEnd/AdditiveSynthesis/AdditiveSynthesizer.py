from BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np
import time
from BackEnd.AdditiveSynthesis.PartialNote import PartialNote
from BackEnd.Note import Note
from BackEnd.Instruments import Instruments

class AdditiveSynthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def create_note_signal(self, note, instrument):
        #start_time = time.time()
        amplitude_array = None
        partials = self.__get_partials__(instrument, note.frequency)
        for i in range(0, len(partials)):
            freq = partials[i].get_freq()
            phase = partials[i].get_phase()
           
            partials[i].get_amplitude_array(note)
            time_vals = np.linspace(0, partials[i].last_time_value, note.fs*partials[i].last_time_value)

            output_sine = partials[i].output_signal * np.sin(
                    freq * 2 * np.pi * (time_vals) +phase*(180/np.pi))

            if i == 0:
                amplitude_array = output_sine
            else:
                difference = len(amplitude_array) - len(output_sine)
                zeros = np.zeros(abs(difference), dtype=np.uint16)
                if (difference > 0):


                    amplitude_array += np.concatenate([output_sine, zeros])
                elif (difference <0):
                    amplitude_array = np.concatenate([amplitude_array, zeros]) +output_sine
                else:
                    amplitude_array += output_sine


        note.output_signal = (note.velocity/(127/2))  * amplitude_array

        #endtime = time.time()

        #print(str(endtime - start_time))
        

    def __get_partials__(self, instrument, frequency):
        freq_of_samples = 261.63

        multiplier = frequency / freq_of_samples
        if (instrument == Instruments.TRUMPET.value[0]):
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

        elif(instrument == Instruments.OBOE.value[0]):
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

        elif (instrument == Instruments.VIOLIN.value[0]):
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
        elif (instrument == Instruments.ACCORDEON.value[0]):
            partial1 = PartialNote(262.3775 * multiplier, 2.151939, 0.01, 0.114, 0.3647, 0.192, 0.339, 3.93, 0.3124, 4.119)

            partial2 = PartialNote(524.755 * multiplier, 0.1374, 0.01, 0.146, 0.379, 0.264, 0.345, 3.93, 0.218, 4.06)

            partial3 = PartialNote(787.13263 * multiplier, -0.2871, 0.01, 0.208, 0.6765, 0.4, 0.65233, 3.93, 0.507, 4.07)

            partial4 = PartialNote(1049.35665 * multiplier, 1.305462, 0.01, 0.0666, 0.205, 0.156, 0.0753, 3.93, 0.0623, 4.08)

            partial5 = PartialNote(1311.7342 * multiplier, 1.722816, 0.01, 0.085, 0.308, 0.286, 0.2635, 3.93, 0.2, 4)

            partial6 = PartialNote(1574.112 * multiplier, -1.35669, 0.01, 0.156, 0.147, 0.3, 0.1287, 3.93, 0.101, 4.08)

            partial8 = PartialNote(2099.02 * multiplier, -2.73082, 0.01, 0.184, 0.036, 0.513, 0.0283, 3.93, 0.017, 4.033)

            partial9 = PartialNote(2361.397896 * multiplier, 1.916575, 0.01, 0.139, 0.051, 0.5843, 0.0371, 3.93, 0.0449, 4.055)

            partial14 = PartialNote(3673.132 * multiplier, -0.82067, 0.01, 0.128, 0.039, 0.254, 0.0339, 3.93, 0.028, 4.06)

            partial15 = PartialNote(3935.5096 * multiplier, -0.02447, 0.01, 0.108, 0.055, 0.32, 0.0486, 3.93, 0.0486, 4.06)

            partial16 = PartialNote(4197.887177 * multiplier, 1.5649835, 0.01, 0.183, 0.044, 0.39, 0.039, 3.93, 0.03, 4.046)

            partial17 = PartialNote(4460.26472 * multiplier, 2.4423946, 0.01, 0.1635, 0.06, 0.29, 0.059, 3.93, 0.049, 4.02)

            partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial8, partial9, partial14,partial15,partial16,partial17]
            #partials = [partial1]
            return partials
