from ProgramaPrincipal.BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np
from ProgramaPrincipal.BackEnd.Track import Track
from ProgramaPrincipal.BackEnd.MidiTrack import MidiTrack
from ProgramaPrincipal.BackEnd.MidiNote import MidiNote


class AdditiveSynthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def synthesize_track(self, track):
        for note in track.midi_track.midi_notes:
            track.output_signal += self.create_note_sig(note, track.time_base, track.instrument)

    def create_note_sig(self, note, time_base, instrument):

        first_zero_values, middle_values, last_zero_values = np.split(time_base.get_time_array(),[
                                                                      time_base.get_tick_index_in_time_array(
                                                                          note.note_on_tick)
                                                                      , time_base.get_tick_index_in_time_array(
                                                                            note.note_off_tick)])

        first_zero_values = [0] * len(first_zero_values)

        last_zero_values = [0] * len(last_zero_values)

        frequencies, amplitudes , phases = instrument.__get_partials__(note.frequency)

        middle_time_values = middle_values.copy()

        for i in range(0, len(frequencies)):
            if i == 0:
                middle_values = amplitudes[i] * np.sin(
                    frequencies[i] * 2 * np.pi * (
                                middle_time_values - time_base.convert_tick_to_time(note.note_on_tick)) + phases[i])
            else:
                middle_values += amplitudes[i] * np.sin(
                    frequencies[i] * 2 * np.pi * (
                                middle_time_values - time_base.convert_tick_to_time(note.note_on_tick))+ phases[i])

        note_signal = np.concatenate([first_zero_values, middle_values, last_zero_values]) * note.velocity
        return note_signal
