import numpy as np
import mido
from mido import MidiFile
from BackEnd.Song import Song
from BackEnd.Track import Track
from BackEnd.Note import Note
from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
from BackEnd.KarplusStrongSynthesis.KS_Synthesis import KS_Synthesizer
from BackEnd.SamplesBasedSynthesis.SBSynthesis import SB_Synthesizer
from BackEnd.Instruments import Instruments


class BackEnd:
    def __init__(self):
        self.additive_synthesizer = AdditiveSynthesizer()
        self.ks_synthesizer = KS_Synthesizer()
        self.sb_synthesizer = SB_Synthesizer()
        self.song = Song()
        self.song.test_without_midi()
        #song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')
        self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')

    #song.generate_output_signal(self, N, arrays_to_add)

    def assign_midi_path(self, midi_file_name):
        self.song.load_midi_file_info(midi_file_name) #SEGUIIIIIIIIIIIIIIR

    def synthesize_note(self, note, instrument):
        if (instrument == Instruments.TRUMPET.value[0] or instrument == Instruments.VIOLIN.value[0] or instrument == Instruments.OBOE.value[0]):
            self.additive_synthesizer.create_note_signal(note, instrument)
        elif (instrument == Instruments.GUITAR.value[0] or instrument == Instruments.DRUM.value[0]):
            self.ks_synthesizer.create_note_signal(note, instrument)
        elif (instrument == Instruments.PIANO.value[0] or instrument == Instruments.CELLO.value[0] or instrument == Instruments.VIOLA.value[0] or instrument == Instruments.MANDOLIN.value[0] or instrument == Instruments.BANJO.value[0]):
            self.sb_synthesizer.create_note_signal(note, instrument)

    def synthesize_track(self, track):
        for note in track.notes:
            self.synthesize_note(note, track.instrument)
        self.generate_output_signal(track.time_base.timeline_length, track.notes, track.time_base.fs)

    def syntesize_entire_song(self, song):
        for track in song.tracks:
            self.synthesize_track(track)
        self.generate_output_signal(song.time_base.timeline_length, song.tracks, song.time_base.fs)

    #N: lango del array de salida (En caso de track, largo del track. En caso de song, largo de la song)
    def generate_output_signal(self, N, arrays_to_add, fs):#usar len(note.note_signal)
        output = np.array([])
        for i in arrays_to_add:
            subarray = i.output_signal
            init_time_index = int(round(i.initial_time * fs))
            index_difference = np.zeros(init_time_index - len(output))
            if init_time_index > len(output):
                output = np.concatenate((output, index_difference))
                output = np.concatenate((output, subarray))
            else:
                superpose , add = np.split(subarray, abs(index_difference))[0],np.split(subarray, abs(index_difference))[1]
                output[init_time_index:] += superpose
                output = np.concatenate((output, add))
        return output[0:N]

    
            


    



    




