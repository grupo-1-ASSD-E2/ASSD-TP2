from BackEnd.SynthesizerAbstract import SynthesizerAbstract
from BackEnd.SamplesBasedSynthesis.SampleFrequencies import get_freq_from_fft
from BackEnd.SamplesBasedSynthesis.SampleAdapting import *
import numpy as np
import soundfile as sf
import os


class SB_Synthesizer(SynthesizerAbstract):

    def __init__ (self):
        self.samples_directory = 'ProgramaPrincipal/BackEnd/SamplesBasedSynthesis/samples/'
        self.my_samples_frecuencies()

    def synthesize_track(self, track):
        for note in track.midi_track.midi_notes:
            track.output_signal += self.create_note_sig(note, track.time_base, track.instrument)

    def create_note_sig(self, note, time_base, instrument):
        closest_note = self.closest_note_search(note.frequency)
        midi_code_note = self.midi_code_from_frec(note.frequency)
        midi_code_closest_note = self.midi_code_from_frec(self.samples_frec_dic[closest_note])
        shift = midi_code_note - round(midi_code_closest_note)
        end = note_scaling(self.data, self.samplerate, shift)
        zeros = [0]*(440118 - len(end))
        return np.concatenate((end,zeros))


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
        '''
        for sample in os.listdir(self.samples_directory):
            try:
                self.data, self.samplerate = sf.read(self.samples_directory + sample)
                self.samples_frec_dic[sample] = get_freq_from_fft(self.data, self.samplerate)
                self.mono = True
            except Exception as e:
                self.data = self.data.sum(axis=1) / 2 #convert data from stereo to mono
                self.data, self.samplerate = sf.read(self.samples_directory + sample)
                self.samples_frec_dic[sample] = get_freq_from_fft(self.data, self.samplerate)
                self.mono = False
        '''
        for sample in os.listdir(self.samples_directory):
            self.data, self.samplerate = sf.read(self.samples_directory + sample)
            self.data = self.data.sum(axis=1) / 2
            self.samples_frec_dic[sample] = get_freq_from_fft(self.data, self.samplerate)

