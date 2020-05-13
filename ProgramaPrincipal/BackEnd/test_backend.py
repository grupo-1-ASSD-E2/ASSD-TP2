from ProgramaPrincipal.BackEnd.AditiveSynthesis.Instruments.Flaute import Flaute
from ProgramaPrincipal.BackEnd.AditiveSynthesis.Instruments.Trumpet import Trumpet
from ProgramaPrincipal.BackEnd.Note import Note
from ProgramaPrincipal.BackEnd.Song import Song
from ProgramaPrincipal.BackEnd.Track import Track
import numpy as np

fs = 44100
duration = 5
t = np.linspace(0, duration, int(fs * duration))  # Produces a 1 second Audio-File

song = Song(t)
trumpet = Trumpet()
track1 = Track(t)

song.add_track(track1)

note1 = Note(t,60, 1)
note2 = Note(t,57,4 )

track1.add_note(note1)
track1.add_note(note2)

track1.assign_instrument(trumpet)

note1.note_off(4)
note2.note_off(5)

song.create_out_signal()

song.play_song(fs)


song.plot_wave(5)


