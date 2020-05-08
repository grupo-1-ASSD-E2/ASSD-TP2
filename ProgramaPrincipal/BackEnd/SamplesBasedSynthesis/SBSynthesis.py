from BackEnd.SynthesizerAbstract import SynthesizerAbstract
from BackEnd.SamplesBasedSynthesis.SampleAdapting import *
import numpy as np
import soundfile as sf
import os
from scipy.io.wavfile import write


class SB_Synthesizer(SynthesizerAbstract):

    def __init__ (self):
        self.samples_directory = 'ProgramaPrincipal/BackEnd/SamplesBasedSynthesis/samples/'
        self.existing_frec_dict()
        self.my_samples_frecuencies()

    def synthesize_track(self, track):
        for note in track.midi_track.midi_notes:
            track.output_signal += self.create_note_sig(note, track.time_base, track.instrument)

    def create_note_sig(self, note, time_base, instrument):
        closest_note = self.closest_note_search(note.frequency)
        midi_code_note = self.midi_code_from_frec(note.frequency)
        midi_code_closest_note = self.midi_code_from_frec(self.samples_frec_dic[closest_note])
        shift = midi_code_note - round(midi_code_closest_note)
        data, samplerate = sf.read(self.samples_directory + closest_note)
        pitched_note = note_scaling(data, samplerate, shift)

        note_length = len(np.linspace(0, note.duration, num=(time_base.fs * note.duration)))
        time_stretched_note = time_stretch(pitched_note, len(pitched_note) / (note_length - 2**11)) #Creates array of specified length

        initial_index = time_base.get_tick_index_in_time_array(note.initial_time)

        amp_values = np.array(time_base.get_time_array())
        amp_values = [0] * len(amp_values)
        return time_stretched_note
        

    def midi_code_from_frec(self, frec):
        '''
        Returns de MIDI code corresponding to the frec
        '''
        return 12 * np.log2(frec * 32 / 440) + 9

    def closest_note_search(self, note_frec):
        '''
        This method searches for the closest sample from the note required
        Returns: The closest sampled note as a string
        '''
        closest_note = min(self.samples_frec_dic, key = lambda v: abs(self.samples_frec_dic[v] - note_frec))
        return closest_note


    def my_samples_frecuencies(self):
        '''
        This method creates a dictionary with samples as key and frecuencies as value
        '''
        self.samples_frec_dic = {}
        for sample in os.listdir(self.samples_directory):
            note_from_file = sample.split(".")        #Remember to always have the sample file in the following format .note.extension
            self.samples_frec_dic[sample] = self.existing_frec[note_from_file[-2]]

    def existing_frec_dict(self):
        self.existing_frec = {}
        letters = ["A0", "Bb0", "B0",
                "C1", "Db1", "D1", "Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1",
				"C2", "Db2", "D2", "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2",
				"C3", "Db3", "D3", "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3",
				"C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4",
				"C5", "Db5", "D5", "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5",
				"C6", "Db6", "D6", "Eb6", "E6", "F6", "Gb6", "G6", "Ab6", "A6", "Bb6", "B6",
				"C7", "Db7", "D7", "Eb7", "E7", "F7", "Gb7", "G7", "Ab7", "A7", "Bb7", "B7",
				"C8"] 
        i=0
        for note in letters:

            prev_freq = round(440/32*(2**(((21+i)-9)/12)), 3)
            self.existing_frec[note] = prev_freq
            i += 1