import numpy as np


from BackEnd.Instruments.Saxo import Saxo
from BackEnd.Instruments.Trumpet import Trumpet
from BackEnd.Instruments.Violin import Violin
from BackEnd.MidiNote import MidiNote
from BackEnd.MidiTrack import MidiTrack
from BackEnd.TimeBase.Tempo import Tempo
from BackEnd.TimeBase.TimeBase import TimeBase
from BackEnd.Track import Track

# from ProgramaPrincipal.BackEnd.Instruments.Saxo import Saxo
# from ProgramaPrincipal.BackEnd.Instruments.Trumpet import Trumpet
# from ProgramaPrincipal.BackEnd.Instruments.Violin import Violin
# from ProgramaPrincipal.BackEnd.MidiNote import MidiNote
# from ProgramaPrincipal.BackEnd.MidiTrack import MidiTrack
# from ProgramaPrincipal.BackEnd.TimeBase.Tempo import Tempo
# from ProgramaPrincipal.BackEnd.TimeBase.TimeBase import TimeBase
# from ProgramaPrincipal.BackEnd.Track import Track

#from Instruments.Saxo import Saxo
#from Instruments.Trumpet import Trumpet
#from Instruments.Violin import Violin
from MidiNote import MidiNote
from MidiTrack import MidiTrack
from TimeBase.Tempo import Tempo
from TimeBase.TimeBase import TimeBase
from Track import Track


import simpleaudio as sa
import matplotlib.pyplot as plt
from scipy.io import wavfile
import mido
from mido import MidiFile


class Song:
    def __init__(self):
        self.song_tracks = []
        self.time_base = None
        self.output_signal = []
        self.output_time_signal = []
        self.midi_file = None

    def set_time_base(self, time_base):
        self.time_base = time_base
        self.output_time_signal = time_base.get_time_array()
        self.output_signal = [0] * self.output_time_signal

        for track in self.song_tracks:
            track.initialize_output_signal_array(time_base)

    def add_track(self, track):
        self.song_tracks.append(track)

    def get_output_signal(self):
        for track in self.song_tracks:
            track.synthesize()
            self.output_signal += track.get_output_signal()

        return self.output_signal

    #def load_from_midi_file(self, midi_file_path, instruments): #instruments para mi no iria
    def load_from_midi_file(self, midi_file_path):
        self.midi_file = MidiFile(midi_file_path, clip=True)
        print('hello from load from midi file')
        #number_of_samples = 0  # get from midi file
        #time_base = TimeBase(number_of_samples)
        #time_base.add_new_tempo(Tempo(1 / 1000000, 0, 1))
        # add tracks
        # add notes

        self.set_time_base(time_base)

    def test_without_midi(self):

        time_base = TimeBase(1000, 44100)
        time_base.add_new_tempo(Tempo(0.005, 0, 499))
        time_base.add_new_tempo(Tempo(0.015, 500, 999))

        track1 = Track()
        track1.assign_instrument(Trumpet())
        track1.initialize_output_signal_array(time_base)

        midi_track = MidiTrack()
        track1.associate_midi_track(midi_track)

        note1 = MidiNote(60, 0, 1, note_off_tick=500)
        note2 = MidiNote(64, 400, 0.5, note_off_tick=600)
        note3 = MidiNote(61, 600, 1, note_off_tick=850)
        note4 = MidiNote(55, 800, 1, note_off_tick=1000)

        midi_track.add_note(note1)
        midi_track.add_note(note2)
        midi_track.add_note(note3)
        midi_track.add_note(note4)
        track1.initialize_output_signal_array(time_base)
        self.add_track(track1)
        self.set_time_base(time_base)

        self.output_signal = self.get_output_signal()
        self.play_song()
        self.plot_wave(10)
        self.plot_spectrum(10000)
        self.plot_phase(10000)

    def play_song(self):

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


    def plot_spectrum(self, finalfreq):

        # plot different spectrum types:

        plt.magnitude_spectrum(self.output_signal, Fs=self.time_base.fs, color='C1')

        plt.xlabel('f(Hz)')
        plt.ylabel('amplitude(A)')

        plt.xlim(0, finalfreq)
        plt.show()

    def plot_phase(self, finalfreq):

        # plot different spectrum types:

        plt.phase_spectrum(self.output_signal, Fs=self.time_base.fs, color='C1')

        plt.xlabel('f(Hz)')
        plt.ylabel('rad')

        plt.xlim(0, finalfreq)
        plt.show()

    def create_wav_file(self, file_name):
        # Start playback
        audio = self.output_signal * (2 ** 15 - 1) / np.max(np.abs(self.output_signal))
        audio = audio.astype(np.int16)
        wavfile.write(file_name, self.time_base.fs, audio)



