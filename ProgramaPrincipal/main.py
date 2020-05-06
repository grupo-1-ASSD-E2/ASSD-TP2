import mido
from mido import MidiFile
import matplotlib.pyplot as plt
import numpy as np
import rtmidi
import simpleaudio as sa
from scipy.io import wavfile

<<<<<<< HEAD
from BackEnd.AditiveSynthesis.ADSR import ADSR

=======
>>>>>>> ff8c467dbbb349475852912ebd2a57d8c61f3664
midiout = rtmidi.MidiOut()
mid = MidiFile('ProgramaPrincipal/Resources/Rodrigo_-_2do_movimiento_Concierto_de_Aranjuez__Adagio.mid', clip=True)
mid1 = MidiFile('ProgramaPrincipal/Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid', clip=True)
mid2 = MidiFile('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid', clip=True)
mid3 = MidiFile('ProgramaPrincipal/Resources/Disney_Themes_-_Under_The_Sea.mid')

fs = 44100
duration = 40
t = np.linspace(0, duration, int(fs * duration))  # Produces a 1 second Audio-File







def print_midi_info():
    # type 0 (single track): all messages are saved in one track
    # type 1 (synchronous): all tracks start at the same time
    # type 2 (asynchronous): each track is independent of the others
    print(mid)
    for track in mid3.tracks:
        print(track)

    for track in mid3.tracks:
        print(track)
        for msg in track:
            print(msg)


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


def plot_sine_wave( y, final_time):
    plt.plot(t, y)
    plt.xlabel('time(s)')
    plt.ylabel('amplitude(A)')

    plt.xlim(0, final_time)
    plt.show()

def plot_spectrum( y):

    plt.xlabel('freq(f)')
    plt.ylabel('amplitude(A)')
    plt.magnitude_spectrum(y, Fs=44100, scale='dB', color='C1')

    plt.show()


def midi_note_to_frequency(note):
    a = 440 #frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))





freqs = [261,523,785,1050,1310,1575]
amplitudes = [0.19,0.22,0.065,0.02,0.03,0.01]
phases = [0.09,0.1685,0.184,2.6,0.9042,1.738]


sine = get_sine_wave(1,440)



#for i in range(0,len(freqs)):
#    sine += get_sine_wave(amplitudes[i], freqs[i], phase= phases[i], cos=True)

#sine = get_sine_wave(0.5,440)
#sine += get_sine_wave(0.2,440)
#sine += get_sine_wave(0.2,550)



print_midi_info()
reproduce_midi_file(mid3)