import numpy as np

from BackEnd.Instruments.Trumpet import Trumpet
from BackEnd.Instruments.Oboe import Oboe
from BackEnd.Instruments.Violin import Violin
#from BackEnd.Instruments.Piano import Piano
from BackEnd.TimeBase.Tempo import Tempo
from BackEnd.TimeBase.TimeBase import TimeBase
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
        print(self.midi_file)
        self.time_base = TimeBase(self.fs)
        ticks_counter = 0
        for msg in self.midi_file.tracks[0]: #saving tempos and time info
            ticks_counter += msg.time
            if msg.type == 'set_tempo':
                new_tempo = Tempo(msg.tempo, self.midi_file.ticks_per_beat, msg.time, ticks_counter)
                self.time_base.add_new_tempo(new_tempo)
                #print(msg.tempo)
                #print(msg.time)   
        track_counter = 1
        for track in self.midi_file.tracks[1::]: #saving tracks and notes info
            new_track = Track()
            ticks_counter = 0
            print('TRACK NUMBER:', track_counter)
            same_time_counter = 0
            notes_still_on_counter = 0
            good_notes_counter = 0
            for counter, msg in enumerate(track):
                ticks_counter += msg.time
                if msg.type == 'note_on': #searching for a note_on
                    if msg.velocity != 0:
                        note_still_on = True
                        ticks_counter1 = 0
                        for msg1 in track[counter::]:
                            ticks_counter1 += msg1.time
                            if note_still_on == True:
                                if ((msg1.type == 'note_off') or ((msg1.type =='note_on') and (msg1.velocity == 0))):
                                    if msg1.note == msg.note: #saving note info after ha corresponding note_off was found
                                        note_still_on = False
                                        t_on = self.time_base.convert_tick_to_time(ticks_counter)
                                        t_off = self.time_base.convert_tick_to_time(ticks_counter1)
                                        note_duration = t_off - t_on
                                        new_note = Note(msg.note, note_duration, msg.velocity, t_on) #Si descartamos las que empiezan y terminan al mismo tiempo, meter esto adentro del if
                                        new_track.add_note(new_note)
                                        if msg1.time == 0:    #CLAVE ESTO CORREGIRLOOOOOOOOO HAY QUE COMPARAR TIEMPOS ABSOLUTOS DE INI Y FIN
                                            good_notes_counter += 1
                                        else:
                                            same_time_counter += 1
                            else:
                                break
                        if note_still_on == True:
                            notes_still_on_counter += 1
            self.tracks.append(new_track)
            track_counter += 1
            print('good_notes_counter', good_notes_counter)
            print('same_time_counter:', same_time_counter)
            print('notes_Still_on_counter:', notes_still_on_counter)


    def test_without_midi(self):
        time_base = TimeBase(1000, 44100) # 1000 seria la cantidad total de ticks de la cancion
        time_base.add_new_tempo(Tempo(0.005, 0, 499)) #entre ticks 0 y 499 el tiempo entre dos ticks es 0.005s
        time_base.add_new_tempo(Tempo(0.015, 500, 999))
        track1 = Track()
        track1.assign_instrument(self.backend.instruments["trumpet"])
        track1.initialize_output_signal_array(time_base)
        midi_track = MidiTrack()
        track1.associate_midi_track(midi_track)

        note1 = MidiNote(60, 1, 1, duration=2)
        note2 = MidiNote(55, 3, 0.5, duration=2)
        note3 = MidiNote(59, 4, 1, duration=1)
        note4 = MidiNote(62, 6, 0.9, duration=2)
        '''
        note5 = MidiNote(62, 500, 1, note_off_tick=700)
        note6 = MidiNote(66, 600, 0.5, note_off_tick=700)
        note7 = MidiNote(51, 700, 1, note_off_tick=850)
        note8 = MidiNote(55, 800, 0.9, note_off_tick=860)
        note9 = MidiNote(63, 900, 1, note_off_tick=990)
        note10 = MidiNote(67, 100, 0.5, note_off_tick=500)
        note11= MidiNote(52, 200, 1, note_off_tick=450)
        note12 = MidiNote(56, 300, 0.9, note_off_tick=950)
        note13 = MidiNote(60, 400, 1, note_off_tick=650)
        note14 = MidiNote(68, 500, 0.5, note_off_tick=620)
        note15= MidiNote(71, 600, 1, note_off_tick=750)
        note16= MidiNote(50, 800, 0.9, note_off_tick=1000)'''

        
        midi_track.add_note(note1)
        
        midi_track.add_note(note2)
        midi_track.add_note(note3)
        midi_track.add_note(note4)
        '''
        midi_track.add_note(note5)

        midi_track.add_note(note6)
        midi_track.add_note(note7)
        midi_track.add_note(note8)
        midi_track.add_note(note9)
        midi_track.add_note(note10)
        midi_track.add_note(note11)
        midi_track.add_note(note12)
        midi_track.add_note(note13)
        midi_track.add_note(note14)
        midi_track.add_note(note15)
        midi_track.add_note(note16)'''

        
        self.add_track(track1)
        self.set_time_base(time_base)
        self.output_signal = self.get_output_signal()
        self.play_song()
        self.plot_wave(10)
        self.plot_spectrum(10000)
        self.plot_phase(10000)

    def play_song(self): #MOVER?
        # Start playback
        audio = self.output_signal * (2 ** 15 - 1) / np.max(np.abs(self.output_signal))
        audio = audio.astype(np.int16)
        play_obj = sa.play_buffer(audio, 1, 2, self.time_base.fs)
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
        plt.magnitude_spectrum(self.output_signal, Fs=self.time_base.fs, color='C1')
        plt.xlabel('f(Hz)')
        plt.ylabel('amplitude(A)')
        plt.xlim(0, finalfreq)
        plt.show()

    def plot_phase(self, finalfreq): #MOVER
        # plot different spectrum types:
        plt.phase_spectrum(self.output_signal, Fs=self.time_base.fs, color='C1')
        plt.xlabel('f(Hz)')
        plt.ylabel('rad')
        plt.xlim(0, finalfreq)
        plt.show()

    def create_wav_file(self, file_name): #MOVER?
        # Start playback
        audio = self.output_signal * (2 ** 15 - 1) / np.max(np.abs(self.output_signal))
        audio = audio.astype(np.int16)
        wavfile.write(file_name, self.time_base.fs, audio)



