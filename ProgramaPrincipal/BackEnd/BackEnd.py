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
from numba import njit
import array


class BackEnd:
    def __init__(self):
        self.additive_synthesizer = AdditiveSynthesizer()
        self.ks_synthesizer = KS_Synthesizer()
        self.sb_synthesizer = SB_Synthesizer()
        self.song = Song()
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Disney_Themes_-_Under_The_Sea.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        self.song.load_midi_file_info('ProgramaPrincipal/Resources/fragmento-rodrigo.mid')

        self.midi_path = 'ProgramaPrincipal/Resources/'

                
        #self.song.load_midi_file_info('Resources/Michael Jackson - Billie Jean.mid')
        #self.song.load_midi_file_info('Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        #self.song.load_midi_file_info('Resources/Queen - Bohemian Rhapsody.mid')
        #self.song.load_midi_file_info('Resources/Disney_Themes_-_Under_The_Sea.mid')

        #Para probar cancion entera
        '''
        for i in range(len(self.song.tracks)):
            self.song.tracks[i].assign_instrument('Piano')
        self.song.tracks[1].assign_instrument('Mandolin')
        self.song.tracks[3].assign_instrument('Viola')
        self.song.tracks[2].assign_instrument('Saxophone')
        #self.song.tracks[4].assign_instrument('Cello')
        #self.song.tracks[6].assign_instrument('Cello')
        #self.song.tracks[7].assign_instrument('Banjo')
        #self.song.tracks[8].assign_instrument('Violin')
        #self.song.tracks[9].assign_instrument('Mandolin')
        #self.song.tracks[10].assign_instrument('Trumpet')
        #self.song.tracks[11].assign_instrument('Oboe')
        
        self.syntesize_entire_song(self.song)
        self.play_signal(self.song.output_signal)
        
        
        #Para probar notas
        '''
        start_time = time.time()
        note = Note(62,8,1,1,44100)
        self.synthesize_note(note, 'Cello')
        print(time.time() - start_time)
        self.play_signal(note.output_signal)
        '''
        
        
        
        #Para probar un track
        
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        #self.song.load_midi_file_info('Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        '''
        self.song.tracks[7].assign_instrument('Piano')
        self.synthesize_track(self.song.tracks[7])
        self.play_signal(self.song.tracks[7].output_signal)'''

    def assign_midi_path(self, midi_file_name):
        self.song.load_midi_file_info(self.midi_path + midi_file_name)
            
    
    #PARA PROBAR
    def play_signal(self, signal): 
        
        # Start playback
        #self.plot_wave(signal, 1000000)
        audio = signal  * (2 ** 15 - 1) / np.max(np.abs(signal))
        audio = audio.astype(np.int16)
        wavfile.write("rodrigosynth.wav", self.song.fs, audio)
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
        elif (instrument == Instruments.PIANO.value[0] or instrument == Instruments.CELLO.value[0] or instrument == Instruments.VIOLA.value[0] or instrument == Instruments.MANDOLIN.value[0] or instrument == Instruments.BANJO.value[0] or instrument == Instruments.BASSOON.value[0] or instrument == Instruments.SAXOPHONE.value[0]):
            self.sb_synthesizer.create_note_signal(note, instrument)

    def synthesize_track(self, track):
        start_time = time.time()
        for note in track.notes:
            self.synthesize_note(note, track.instrument)
        print('track synthesis:',time.time() - start_time)
        track.output_signal = self.generate_output_signal(track.time_base.timeline_length, track.notes, track.time_base.fs, delete_subarrays_after_generation=True)

    def syntesize_entire_song(self, song):
        song_activated_tracks = []
        for track in song.tracks:
            if track.activated:
                self.synthesize_track(track)
                song_activated_tracks.append(track)
        song.output_signal = self.generate_output_signal(song.time_base.timeline_length, song_activated_tracks, song.time_base.fs, delete_subarrays_after_generation=True)

    #N: lango del array de salida (En caso de track, largo del track. En caso de song, largo de la song)
    
    def generate_output_signal(self, N, arrays_to_add, fs, delete_subarrays_after_generation = False):#usar len(note.note_signal)
        start_time = time.time()
        output = np.array([])
        for i in arrays_to_add:
            if len(i.output_signal) != 0: 
                init_time_index = int(round(i.initial_time * fs))
                index_difference = init_time_index - len(output)
                if init_time_index >= len(output):
                    zero_padd = np.zeros(index_difference)
                    output = np.concatenate([output, zero_padd, i.output_signal])
                    if delete_subarrays_after_generation:
                        i.output_signal=np.array([])
                    
                else:
                    if abs(index_difference) >= len(i.output_signal):
                        output[init_time_index:len(i.output_signal) + init_time_index] += i.output_signal
                        if delete_subarrays_after_generation:
                            i.output_signal=np.array([])
                    else:
                        superpose, add = np.split(i.output_signal, [abs(index_difference)])
                        if delete_subarrays_after_generation:
                            i.output_signal=np.array([])
                        output[init_time_index:] += superpose
                        superpose = None
                        output = np.concatenate((output, add))
                        add = None
        print('Generate function: ', time.time()-start_time)
        return output[0:N]
    

