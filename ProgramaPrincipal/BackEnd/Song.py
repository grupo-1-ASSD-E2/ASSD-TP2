import simpleaudio as sa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class Song:
    def __init__(self, time_array):
        self.tracks = []
        self.time_array = time_array
        self.out_signal = []

    def add_track(self, track):
        track.time_array = self.time_array
        self.tracks.append(track)

    def create_out_signal(self):

        for i in range(0, len(self.tracks)):
            self.tracks[i].create_out_signal()
            if i == 0:
                self.out_signal = self.tracks[i].out_signal
            else:
                self.out_signal += self.tracks[i].out_signal

    def play_song(self, fs):
        # Start playback
        audio = self.out_signal * (2 ** 15 - 1) / np.max(np.abs(self.out_signal))
        audio = audio.astype(np.int16)


        play_obj = sa.play_buffer(audio, 1, 2, fs)

        # Wait for playback to finish before exiting
        play_obj.wait_done()


    def plot_wave(self, final_time):
        plt.plot(self.time_array, self.out_signal)
        plt.xlabel('time(s)')
        plt.ylabel('amplitude(A)')

        plt.xlim(0, final_time)
        plt.show()

    def create_wav_file(self, file_name, fs):
        # Start playback
        audio = 0.5 * self.out_signal * (2 ** 15 - 1) / np.max(np.abs(self.out_signal))
        audio = audio.astype(np.int16)
        wavfile.write(file_name, fs, audio)