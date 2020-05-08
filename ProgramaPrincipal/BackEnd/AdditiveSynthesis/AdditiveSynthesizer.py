from BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np
import time

class AdditiveSynthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def create_note_signal(self, note, instrument):
        start_time = time.time()
        amplitude_array = None
        partials = instrument.__get_partials__(note.frequency)
        for i in range(0, len(partials)):
            if i == 0:
                amplitude_array = partials[i].output_signal
            else:
                amplitude_array  = partials[i].output_signal

        '''
        amp_values = np.array(time_base.get_time_array())

        time_values = amp_values.copy()

        amp_values = [0] * len(amp_values)  # initialize

        partials = instrument.__get_partials__(note.frequency)

        for i in range(0, len(partials)):
            amplitude_array = partials[i].get_amplitude_array(note, time_base)
            freq = partials[i].get_freq()
            phase = partials[i].get_phase()
            if i == 0:
                amp_values = amplitude_array * np.sin(
                    freq * 2 * np.pi * (time_values - note.initial_time) +phase*(180/np.pi))
            else:
                amp_values += amplitude_array * np.sin(
                    freq * 2 * np.pi * (time_values - note.initial_time) +phase*(180/np.pi))

        note_signal = amp_values * note.velocity
        '''




        endtime = time.time()

        print(str(endtime - start_time))
        note.output_signal = note_signal
