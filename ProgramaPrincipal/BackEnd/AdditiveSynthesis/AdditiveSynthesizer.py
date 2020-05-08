from BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np

class AdditiveSynthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def synthesize_track(self, track):
        i = 1
        for note in track.midi_track.midi_notes:
            track.output_signal += self.create_note_sig(note, track.time_base, track.instrument)
            print(str(i))
            i+=1

    def create_note_sig(self, note, time_base, instrument):

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
        return note_signal
