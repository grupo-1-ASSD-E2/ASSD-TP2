
from BackEnd.Instruments.Trumpet import Trumpet
from BackEnd.Instruments.Violin import Violin
from BackEnd.Song import Song

from BackEnd.Song import Song
import mido
from mido import MidiFile
from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
from BackEnd.Instruments.Oboe import Oboe


class BackEnd:
    def __init__(self):
        self.additive_synthesizer = AdditiveSynthesizer()
    
        self.instruments = {"trumpet" : Trumpet(self.additive_synthesizer),
                            "violin": Violin(self.additive_synthesizer),
                            "oboe": Oboe(self.additive_synthesizer)}
        song = Song(self)
        song.test_without_midi()
        #song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')


    def generate_output_signal(self, N, arrays_to_add):#usar len(note.note_signal)
        for sub_array in arrays_to_add.:
            note_to_add = self.create_note_signal(note, track.time_base, track.instrument)
            otuput_track = note_to_add


