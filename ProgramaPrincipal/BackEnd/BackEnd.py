from ProgramaPrincipal.BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
from ProgramaPrincipal.BackEnd.Instruments.Trumpet import Trumpet
from ProgramaPrincipal.BackEnd.Instruments.Violin import Violin
from ProgramaPrincipal.BackEnd.Song import Song


class BackEnd:
    def __init__(self):
        self.instruments = [Trumpet(), Violin()]

        song = Song()
        song.test_without_midi()


backend = BackEnd()



