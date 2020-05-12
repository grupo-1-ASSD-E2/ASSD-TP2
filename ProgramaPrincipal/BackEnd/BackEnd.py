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
        self.counter = 0
        self.song = Song()
        self.midi_path = 'ProgramaPrincipal/Resources/'
        self.play_obj = None

        #PABLO GONZA
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/faded.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/badguy.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Disney_Themes_-_Under_The_Sea.mid')
        #self.song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        self.song.load_midi_file_info('Resources/fragmento-rodrigo.mid')

        #MALE
        #self.song.load_midi_file_info('Resources/Michael Jackson - Billie Jean.mid')
        #self.song.load_midi_file_info('Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid')
        #self.song.load_midi_file_info('Resources/Queen - Bohemian Rhapsody.mid')
        #self.song.load_midi_file_info('Resources/Disney_Themes_-_Under_The_Sea.mid')
        #self.song.load_midi_file_info('Resources/faded.mid')

        #self.test_song()


    def test_note(self):
        #Para probar notas
        note = Note(62,8,1,1,44100)
        self.synthesize_note(note, 'Cello')
        self.play_signal(note.output_signal)
        

    def test_track(self):
        #Para probar un track
        
        self.song.tracks[7].assign_instrument('Piano')
        self.synthesize_track(self.song.tracks[7])
        self.play_signal(self.song.tracks[7].output_signal)
        
    def test_song(self):
        #Para probar cancion entera
        '''
        for i in range(len(self.song.tracks)):
            self.song.tracks[i].assign_instrument('Accordeon')
        '''
        
        self.song.tracks[0].assign_instrument('Piano')
        '''
        self.song.tracks[1].assign_instrument('Mandolin')
        self.song.tracks[3].assign_instrument('Violin')
        self.song.tracks[2].assign_instrument('Saxophone')
        self.song.tracks[4].assign_instrument('Cello')
        self.song.tracks[6].assign_instrument('Basoon')
        self.song.tracks[5].assign_instrument('Accordeon')
        self.song.tracks[7].assign_instrument('Banjo')'''
        '''
        self.song.tracks[8].assign_instrument('Violin')
        self.song.tracks[9].assign_instrument('Mandolin')
        self.song.tracks[10].assign_instrument('Trumpet')
        self.song.tracks[11].assign_instrument('Oboe')
        self.song.tracks[12].assign_instrument('Guitar')
        self.song.tracks[13].assign_instrument('Mandolin')
        self.song.tracks[14].assign_instrument('Viola')
        self.song.tracks[15].assign_instrument('Saxophone')
        self.song.tracks[16].assign_instrument('Cello')
        self.song.tracks[17].assign_instrument('Piano')
        self.song.tracks[18].assign_instrument('Piano')
        self.song.tracks[19].assign_instrument('Banjo')
        self.song.tracks[20].assign_instrument('Violin')'''

        self.syntesize_entire_song(self.song)
        #self.play_signal(self.song.output_signal)


    def assign_midi_path(self, midi_file_name):
        self.song.load_midi_file_info(self.midi_path + midi_file_name)
            
    
    #PARA PROBAR
    def play_signal(self, signal): 
        
        # Start playback
        #self.plot_wave(signal, 1000000)
        audio = signal  * (2 ** 15 - 1) / np.max(np.abs(signal))
        audio = audio.astype(np.int16)
        
        self.play_obj = sa.play_buffer(audio, 1, 2, self.song.fs)
        # Wait for playback to finish before exiting
        #play_obj.wait_done() 

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
            if (track.has_changed):
                self.synthesize_note(note, track.instrument)
                track.output_signal = self.generate_output_signal(track.time_base.timeline_length, note, track.time_base.fs, delete_subarrays_after_generation=True, output_array=track.output_signal)
            else:
                ##Load track from file
                i = 0

        track.has_changed = False
        print('track synthesis:',time.time() - start_time)
        #track.output_signal = self.generate_output_signal(track.time_base.timeline_length, track.notes, track.time_base.fs, delete_subarrays_after_generation=True)

    def syntesize_entire_song(self, song):
        song_activated_tracks = []
        it = 0
        for track in song.tracks:
            print(str(it))
            it +=1
            if track.activated:
                self.synthesize_track(track)
                song.output_signal = self.generate_output_signal(song.time_base.timeline_length, track, song.time_base.fs, delete_subarrays_after_generation=True, output_array=song.output_signal)
                song_activated_tracks.append(track)
        

    def generate_output_signal(self, N, array_to_add, fs, delete_subarrays_after_generation = False, output_array = np.array([])):#usar len(note.note_signal)
        
        #start_time = time.time()
        output = output_array
        volume_normalize = 1
        if len(array_to_add.output_signal) > 0 and np.max(array_to_add.output_signal) is not 0:
            volume_normalize = 1.0 / np.amax(array_to_add.output_signal)
        if len(array_to_add.output_signal) != 0: 
            init_time_index = int(round(array_to_add.initial_time * fs))
            index_difference = init_time_index - len(output)
            if init_time_index >= len(output):
                zero_padd = np.zeros(index_difference, dtype=np.uint8)
                output = np.concatenate([output, zero_padd, array_to_add.output_signal * (array_to_add.velocity / (127 * 2)) * volume_normalize])
                if delete_subarrays_after_generation:
                    array_to_add.output_signal = None
                
            else:
                if abs(index_difference) >= len(array_to_add.output_signal):
                    output[init_time_index:len(array_to_add.output_signal) + init_time_index] += array_to_add.output_signal * (array_to_add.velocity / (127 * 2)) * volume_normalize
                    if delete_subarrays_after_generation:
                        array_to_add.output_signal = None
                else:
                    superpose, add = np.split(array_to_add.output_signal, [abs(index_difference)])
                    if delete_subarrays_after_generation:
                        array_to_add.output_signal = None
                    output[init_time_index:] += superpose * (array_to_add.velocity / (127 * 2)) * volume_normalize
                    superpose = None
                    output = np.concatenate((output, add * (array_to_add.velocity / (127 * 2)) * volume_normalize))
                    add = None
        #print('Generate function: ', time.time()-start_time)
        #np.save('ProgramaPrincipal/BackEnd/Tracks/' + 'track' + str(self.counter) + '.npy', output[0:N])
        self.counter += 1
        return output




    #########################CONEXION CON FRONT-END###################################

    def load_midi_file(self, file_path):
        ####Chequear que exista el PATH###
        self.song.load_midi_file_info(file_path)

    def get_track_list(self):
        return self.song.tracks

    def get_instrument_list(self):
        return Instruments.list()

    def assign_instrument_to_track(self, n_of_track, instrument, volume):
        if (n_of_track < len(self.song.tracks)):
            self.song.tracks[n_of_track].assign_instrument(instrument)
            self.song.tracks[n_of_track].set_volume(volume)

    def synthesize_song(self):
        if (self.song is not None):
            self.syntesize_entire_song(self.song)
        else:
            return -1

    def play_song(self):
        if (self.song.output_signal is not None):
            self.play_signal(self.song.output_signal)
        else: 
            return -1

    def play_track(self, n_of_track):
        if self.song is not None:
            if (n_of_track < len(self.song.tracks)):
                self.synthesize_track(self.song.tracks[n_of_track])
                if (self.song.tracks[n_of_track].output_signal is not None):
                    self.play_signal(self.song.tracks[n_of_track].output_signal)
                else: 
                    return -1
            else:
                return -1
        else:
            return -1
        

    def toggle_track(self, n_of_track):
        if (n_of_track < len(self.song.tracks)):
            self.song.track[n_of_track].toggle_track()

    def create_chord(self, list_of_notes):
        #Ver como es el parametro list_of_notes
        raise NotImplementedError("Not Implemented")

    def pause_reproduction(self):
        self.play_obj.stop()

    def continue_reproduction(self):
        self.play_obj.play()

    def stop_reproduction(self):
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()


    def save_as_wav_file(self, filename):
        if (self.song is not None and self.song.output_signal is not None):
            audio = self.song.output_signal  * (2 ** 15 - 1) / np.max(np.abs(self.song.output_signal))
            audio = audio.astype(np.int16)
            wavfile.write(filename, self.song.fs, audio)
        else:
            return -1
        

    def save_as_mp3_file(self, filename):
        raise NotImplementedError("Not Implemented")

    def plot_spectrogram(self):
        raise NotImplementedError("Not Implemented")
    
        
            


