#from ProgramaPrincipal.BackEnd.Instruments.Trumpet import Trumpet
#from ProgramaPrincipal.BackEnd.Instruments.Violin import Violin
#from ProgramaPrincipal.BackEnd.Song import Song

#from Instruments.Trumpet import Trumpet
#from Instruments.Violin import Violin
from Song import Song
import mido
from mido import MidiFile


class BackEnd:
    def __init__(self):
        #self.instruments = [Trumpet(), Violin()]
        song = Song()
        #song.test_without_midi()
        song.load_from_midi_file('Resources/Movie_Themes_-_Toy_Story.mid')


backend = BackEnd()



