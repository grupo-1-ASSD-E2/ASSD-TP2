import mido
from mido import MidiFile
from BackEnd.Song import Song
from BackEnd.AdditiveSynthesis.AdditiveSynthesizer import AdditiveSynthesizer
from BackEnd.KarplusStrongSynthesis.KS_Synthesis import KS_Synthesizer
from BackEnd.SamplesBasedSynthesis.SBSynthesis import SB_Synthesizer
from BackEnd.Instruments.Trumpet import Trumpet
from BackEnd.Instruments.Violin import Violin
from BackEnd.Instruments.Oboe import Oboe
from BackEnd.Instruments.Guitar import Guitar
from BackEnd.Instruments.Drum import Drum
from BackEnd.Instruments.Piano import Piano


class BackEnd:
    def __init__(self):
        self.additive_synthesizer = AdditiveSynthesizer()
        self.ks_synthesizer = KS_Synthesizer()
        self.sb_synthesizer = SB_Synthesizer()
    
        self.instruments = {"trumpet" : Trumpet(self.additive_synthesizer),
                            "violin": Violin(self.additive_synthesizer),
                            "oboe": Oboe(self.additive_synthesizer),
                            "guitar": Guitar(self.ks_synthesizer),
                            "drum": Drum(self.ks_synthesizer),
                            "piano": Piano(self.sb_synthesizer)}
        song = Song(self)
        song.test_without_midi()
        #song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')
    




