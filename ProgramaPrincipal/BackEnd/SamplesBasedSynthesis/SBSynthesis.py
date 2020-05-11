'''
from BackEnd.SynthesizerAbstract import SynthesizerAbstract
from BackEnd.SamplesBasedSynthesis.SampleAdapting import *
from BackEnd.Instruments import Instruments
'''
from BackEnd.SynthesizerAbstract import SynthesizerAbstract
from BackEnd.SamplesBasedSynthesis.SampleAdapting import *
from BackEnd.Instruments import Instruments

import numpy as np
import soundfile as sf
import os
import time



class SB_Synthesizer(SynthesizerAbstract):

    def __init__ (self):
        start_time = time.time()
        self.existing_frec_dict()
        self.instrument = 'Piano'
        self.samples_directory = 'ProgramaPrincipal/BackEnd/SamplesBasedSynthesis/samples/' + self.instrument + '/'
        self.my_samples_frecuencies()
        print(time.time() - start_time)

    def create_note_signal(self, note, instrument):
        #If the instrument changes, search new samples
        self.init_instrument_samples(instrument)

        #Look for the closest note in the samples and calculate the shifts required
        closest_note = self.closest_note_search(note.frequency)
        midi_code_note = self.midi_code_from_frec(note.frequency)
        midi_code_closest_note = self.midi_code_from_frec(self.samples_frec_dic[closest_note])
        shift = midi_code_note - round(midi_code_closest_note)
        data, samplerate = sf.read(self.samples_directory + closest_note)
        note_length = int(round(note.fs * note.duration))
        #Pitch the sample to create the required note
        #start_time = time.time()
        if int(shift) != 0:
            if note.duration == 0.0:
                note.output_signal = []
            else:
                time_factor = len(data)/note_length
                pitched_note = note_scaling(data, samplerate, shift, time_factor)
                volume_normalize = 1.0 / np.amax(pitched_note)
                note.output_signal = pitched_note * note.velocity / 127  * volume_normalize
        else:
            
            if note.duration == 0.0:
                note.output_signal = []
            else:
                scaling_factor = len(data)/note_length
                time_stretched_note = stretch(data, scaling_factor)
                volume_normalize = 1.0 / np.amax(time_stretched_note)
                note.output_signal = time_stretched_note * note.velocity / 127 * volume_normalize
            
        
    def init_instrument_samples(self, instrument):
        if self.instrument != instrument:
            self.instrument = instrument
            self.samples_directory = 'ProgramaPrincipal/BackEnd/SamplesBasedSynthesis/samples/' + self.instrument + '/'
            self.my_samples_frecuencies()            

    
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