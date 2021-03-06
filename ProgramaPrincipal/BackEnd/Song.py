import numpy as np
from BackEnd.TimeBase.Tempo import Tempo
from BackEnd.TimeBase.TimeBase import TimeBase
from BackEnd.Note import Note
from BackEnd.Track import Track
import simpleaudio as sa
import matplotlib.pyplot as plt
from scipy.io import wavfile
import mido
from mido import MidiFile
import operator
from BackEnd.Note import Note


class Song:
    def __init__(self):
        self.tracks = []
        self.time_base = None
        self.output_signal = []
        self.output_time_signal = []
        self.midi_file = None
        self.fs = 44100
        self.song_duration = 0
        #self.backend = backend

    def set_time_base(self, time_base):
        self.time_base = time_base
        self.output_time_signal = time_base.get_time_array()
        self.output_signal = [0] * self.output_time_signal
        for track in self.tracks:
            track.initialize_output_signal_array(time_base)

    def add_track(self, track):
        self.tracks.append(track)

    def get_output_signal(self):
        for track in self.tracks:
            track.synthesize()
            self.output_signal += track.get_output_signal()
        return self.output_signal

    #def load_from_midi_file(self, midi_file_path, instruments): #instruments para mi no iria

    def load_midi_file_info(self, midi_file_path):
        self.midi_file = MidiFile(midi_file_path, clip=True)
        self.tracks.clear()
        print(self.midi_file)
        self.time_base = TimeBase(self.fs)
        ticks_counter = 0
        prev_tempo = 0.5
        first_set_tempo = True
        prev_ending = 0
        '''
        for msg in self.midi_file.tracks[0]:
            print(msg)
        '''
        #print('--------------------')
        for msg in self.midi_file.tracks[0]: #saving tempos and time info
            ticks_counter += msg.time
            if msg.type == 'set_tempo' and ticks_counter != 0: # and msg.time != 0:
                if first_set_tempo == True:
                    new_tempo = Tempo(prev_tempo, self.midi_file.ticks_per_beat, ticks_counter - prev_ending, 0)
                    first_set_tempo = False
                    prev_tempo = msg.tempo
                else:
                    new_tempo = Tempo(prev_tempo, self.midi_file.ticks_per_beat, ticks_counter - (prev_ending + 1), prev_ending + 1)
                    prev_tempo = msg.tempo
                self.time_base.add_new_tempo(new_tempo)
                prev_ending = new_tempo.end_tick
            elif msg.type == 'set_tempo' and ticks_counter == 0:
                prev_tempo = msg.tempo 
        total_song_ticks = 0
        for track in self.midi_file.tracks[1:]:
            total_track_ticks = 0
            for msg in track:
                total_track_ticks += msg.time
            if total_track_ticks > total_song_ticks:
                total_song_ticks = total_track_ticks

        if first_set_tempo == True:
            last_tempo = Tempo(prev_tempo, self.midi_file.ticks_per_beat, total_song_ticks - prev_ending, 0)
        else:
            last_tempo = Tempo(prev_tempo, self.midi_file.ticks_per_beat, total_song_ticks - prev_ending, prev_ending + 1)
        self.time_base.add_new_tempo(last_tempo)
        self.song_duration = self.time_base.convert_tick_to_time(total_song_ticks)
        print('total song ticks:', total_song_ticks)
        print('last tempo:', last_tempo.tempo)
        print('last tempo start', last_tempo.start_tick)
        print('last tempo ending:', last_tempo.end_tick)
        #------------------------------------
        track_counter = 1
        for track in self.midi_file.tracks[1:]: #saving tracks and notes info
            new_track = Track()
            new_track.time_base = self.time_base
            ticks_counter = 0
            #same_time_counter = 0
            notes_still_on_counter = 0
            good_notes_counter = 0
            for counter, msg in enumerate(track):
                ticks_counter += msg.time
                if msg.type == 'note_on': #searching for a note_on
                    if msg.velocity != 0:
                        note_still_on = True
                        ticks_counter1 = ticks_counter
                        for msg1 in track[(counter+1)::]:
                            ticks_counter1 += msg1.time
                            if note_still_on == True:
                                if ((msg1.type == 'note_off') or ((msg1.type =='note_on') and (msg1.velocity == 0))):
                                    if msg1.note == msg.note: #saving note info after a corresponding note_off was found
                                        note_still_on = False
                                        t_on = self.time_base.convert_tick_to_time(ticks_counter)
                                        t_off = self.time_base.convert_tick_to_time(ticks_counter1)
                                        note_duration = t_off - t_on
                                        if note_duration > 0:
                                            new_note = Note(msg.note, note_duration, msg.velocity, t_on, self.fs) #Si descartamos las que empiezan y terminan al mismo tiempo, meter esto adentro del if
                                            new_track.add_note(new_note)
                                            good_notes_counter += 1
                            else:
                                break
                        if note_still_on == True:
                            notes_still_on_counter += 1
            print('good notes counter:', good_notes_counter)
            if good_notes_counter > 0:
                self.tracks.append(new_track)
                track_counter += 1
        print('track counter:', track_counter)

    def play_song(self): #MOVER?
        # Start playback
        audio = self.output_signal * (2 ** 15 - 1) / np.max(np.abs(self.output_signal))
        audio = audio.astype(np.int16)
        play_obj = sa.play_buffer(audio, 1, 2, self.fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()

    def plot_wave(self, final_time):
        plt.plot(self.output_time_signal, self.output_signal)
        plt.xlabel('time(s)')
        plt.ylabel('amplitude(A)')
        plt.xlim(0, final_time)
        plt.show()


    def plot_spectrum(self, finalfreq): #MOVER
        # plot different spectrum types:
        plt.magnitude_spectrum(self.output_signal, Fs=self.fs, color='C1')
        plt.xlabel('f(Hz)')
        plt.ylabel('amplitude(A)')
        plt.xlim(0, finalfreq)
        plt.show()

    def plot_phase(self, finalfreq): #MOVER
        # plot different spectrum types:
        plt.phase_spectrum(self.output_signal, Fs=self.fs, color='C1')
        plt.xlabel('f(Hz)')
        plt.ylabel('rad')
        plt.xlim(0, finalfreq)
        plt.show()

    def create_wav_file(self, file_name): #MOVER?
        # Start playback
        audio = self.output_signal * (2 ** 15 - 1) / np.max(np.abs(self.output_signal))
        audio = audio.astype(np.int16)
        wavfile.write(file_name, self.fs, audio)



