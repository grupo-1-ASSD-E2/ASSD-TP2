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
 
        #song.load_midi_file_info('Resources/Rodrigo_-_2do_movimiento_Concierto_de_Aranjuez__Adagio.mid')
        song.load_midi_file_info('Resources/Disney_Themes_-_Under_The_Sea.mid')


backend = BackEnd()



