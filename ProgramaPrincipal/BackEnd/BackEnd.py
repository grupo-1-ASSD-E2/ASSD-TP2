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
import matplotlib.pyplot as plt
from scipy.io import wavfile
import simpleaudio as sa
import time


class BackEnd:
    def __init__(self):
        self.additive_synthesizer = AdditiveSynthesizer()
        self.ks_synthesizer = KS_Synthesizer()
        self.sb_synthesizer = SB_Synthesizer()
        self.song = Song()
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Disney_Themes_-_Under_The_Sea.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        self.midi_path = 'ProgramaPrincipal/Resources/'

        #Para probar cancion entera
        '''
        self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        for i in range(9):
            self.song.tracks[i].assign_instrument('Violin')
        self.syntesize_entire_song(self.song)
        self.play_signal(self.song.output_signal)
        '''

        #Para probar notas
        start_time = time.time()
        note = Note(62,8,1,1,44100)
        self.synthesize_note(note, 'Cello')
        print(time.time() - start_time)
        self.play_signal(note.output_signal)
        
        
        
        #Para probar un track
        '''
        self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        self.song.tracks[5].assign_instrument('Accordeon')
        self.synthesize_track(self.song.tracks[5])
        self.play_signal(self.song.tracks[5].output_signal)
        '''

    def assign_midi_path(self, midi_file_name):
        self.song.load_midi_file_info(self.midi_path + midi_file_name)

#PARA PROBAR
    def play_signal(self, signal): 
        # Start playback
        #self.plot_wave(signal, 1000000)
        audio = signal  * (2 ** 15 - 1) / np.max(np.abs(signal))
        audio = audio.astype(np.int16)
        wavfile.write("metodo3.wav", self.song.fs, audio)
        play_obj = sa.play_buffer(audio, 1, 2, self.song.fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done() 

    def plot_wave(self,signal, final_time):
        plt.plot( signal)
        plt.xlabel('time(s)')
        plt.ylabel('amplitude(A)')
        plt.xlim(0, final_time)
        plt.show()


    def synthesize_note(self, note, instrument):
        if (instrument == Instruments.TRUMPET.value[0] or instrument == Instruments.VIOLIN.value[0] or instrument == Instruments.OBOE.value[0]) or instrument == Instruments.ACCORDEON.value[0]:
            self.additive_synthesizer.create_note_signal(note, instrument)
        elif (instrument == Instruments.GUITAR.value[0] or instrument == Instruments.DRUM.value[0]):
            self.ks_synthesizer.create_note_signal(note, instrument)
        elif (instrument == Instruments.PIANO.value[0] or instrument == Instruments.CELLO.value[0] or instrument == Instruments.VIOLA.value[0] or instrument == Instruments.MANDOLIN.value[0] or instrument == Instruments.BANJO.value[0]):
            self.sb_synthesizer.create_note_signal(note, instrument)

    def synthesize_track(self, track):
        for note in track.notes:
            self.synthesize_note(note, track.instrument)
        track.output_signal = self.generate_output_signal(track.time_base.timeline_length, track.notes, track.time_base.fs)

    def syntesize_entire_song(self, song):
        i = 0
        for track in song.tracks:
            print(str(i))
            i+=1
            self.synthesize_track(track)
        song.output_signal = self.generate_output_signal(song.time_base.timeline_length, song.tracks, song.time_base.fs)

    #N: lango del array de salida (En caso de track, largo del track. En caso de song, largo de la song)
    def generate_output_signal(self, N, arrays_to_add, fs):#usar len(note.note_signal)
        output = np.array([])
        for i in arrays_to_add:
            subarray = i.output_signal
            if len(subarray) != 0: 
                init_time_index = int(round(i.initial_time * fs))
                index_difference = init_time_index - len(output)
                if init_time_index >= len(output):
                    zero_padd = np.zeros(index_difference)
                    output = np.concatenate((output, zero_padd))
                    output = np.concatenate((output, subarray))
                else:
                    if abs(index_difference) >= len(subarray):
                        output[init_time_index:len(subarray) + init_time_index] += subarray
                    else:
                        superpose, add = np.split(subarray, [abs(index_difference)])
                        output[init_time_index:] += superpose
                        output = np.concatenate((output, add))
        return output[0:N]

    
            


    



    




