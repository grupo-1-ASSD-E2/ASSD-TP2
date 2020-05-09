import mido
from mido import MidiFile
import matplotlib.pyplot as plt
import numpy as np
import rtmidi
import simpleaudio as sa
from scipy.io import wavfile
from BackEnd.BackEnd import BackEnd


midiout = rtmidi.MidiOut()

# mid = MidiFile('ProgramaPrincipal/Resources/Rodrigo_-_2do_movimiento_Concierto_de_Aranjuez__Adagio.mid', clip=True)
# mid1 = MidiFile('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid', clip=True)
# mid2 = MidiFile('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid', clip=True)
# mid3 = MidiFile('ProgramaPrincipal/Resources/Disney_Themes_-_Under_The_Sea.mid')


fs = 44100
duration = 40
t = np.linspace(0, duration, int(round(fs * duration))) # Produces a 1 second Audio-File

    # type 0 (single track): all messages are saved in one track
    # type 1 (synchronous): all tracks start at the same time
    # type 2 (asynchronous): each track is independent of the others

# To reproduce midi file
def reproduce_midi_file(midi_file):
    out = mido.get_output_names()[0]
    port = mido.open_output(out)
    for msg in midi_file.play():
        port.send(msg)

# volume range [0.0, 1.0]
# f sine frequency, Hz, may be float
# phase in radians
def get_sine_wave(volume, f, phase=0, cos=False):
    if cos == False:
        y = np.sin(f * 2 * np.pi * t +phase)  # Has frequency of 440Hz
    else:
        y = np.cos(f * 2 * np.pi * t + phase)
        # Ensure that highest value is in 16-bit range



    audio = volume * y * (2 ** 15 - 1) / np.max(np.abs(y))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    return audio


# To reproduce sine waves

def play_sine_wave(audio):

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()


def create_wav_file(file_name, fs, audio):
    wavfile.write(file_name, fs, audio)

#print_midi_info()
#reproduce_midi_file(mid3)

backend = BackEnd()
