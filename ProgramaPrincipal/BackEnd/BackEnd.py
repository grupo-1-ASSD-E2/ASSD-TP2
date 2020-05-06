from BackEnd.Instruments.Trumpet import Trumpet
from BackEnd.Instruments.Violin import Violin
from BackEnd.Song import Song


class BackEnd:
    def __init__(self):
        self.instruments = [Trumpet(), Violin()]

        song = Song()
        song.test_without_midi()





