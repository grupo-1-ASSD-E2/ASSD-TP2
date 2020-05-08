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
from BackEnd.TimeBase.TimeBase import TimeBase
from BackEnd.TimeBase.Tempo import Tempo
from BackEnd.Track import Track
from BackEnd.Note import Note


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
        
        self.test_without_midi()
        #song.load_midi_file_info('ProgramaPrincipal/Resources/Movie_Themes_-_Toy_Story.mid')

    def test_without_midi(self):
        song = Song(self)


        time_base = TimeBase(44100) # 1000 seria la cantidad total de ticks de la cancion
        time_base.add_new_tempo(Tempo(0.005, 0, 499)) #entre ticks 0 y 499 el tiempo entre dos ticks es 0.005s
        time_base.add_new_tempo(Tempo(0.015, 500, 999))


        track1 = Track()
        track1.assign_instrument(self.instruments["trumpet"])
        track1.initialize_output_signal_array(time_base)
        
        midi_track = Track()
        track1.associate_midi_track(midi_track)

        note1 = Note(60, 1, 1, duration=2)
        note2 = Note(55, 3, 0.5, duration=2)
        note3 = Note(59, 4, 1, duration=1)
        note4 = Note(62, 6, 0.9, duration=2)
        '''
        note5 = Note(62, 500, 1, note_off_tick=700)
        note6 = Note(66, 600, 0.5, note_off_tick=700)
        note7 = Note(51, 700, 1, note_off_tick=850)
        note8 = Note(55, 800, 0.9, note_off_tick=860)
        note9 = Note(63, 900, 1, note_off_tick=990)
        note10 = Note(67, 100, 0.5, note_off_tick=500)
        note11= Note(52, 200, 1, note_off_tick=450)
        note12 = Note(56, 300, 0.9, note_off_tick=950)
        note13 = Note(60, 400, 1, note_off_tick=650)
        note14 = Note(68, 500, 0.5, note_off_tick=620)
        note15= Note(71, 600, 1, note_off_tick=750)
        note16= Note(50, 800, 0.9, note_off_tick=1000)'''

        
        midi_track.add_note(note1)
        
        midi_track.add_note(note2)
        midi_track.add_note(note3)
        midi_track.add_note(note4)
        '''
        midi_track.add_note(note5)

        midi_track.add_note(note6)
        midi_track.add_note(note7)
        midi_track.add_note(note8)
        midi_track.add_note(note9)
        midi_track.add_note(note10)
        midi_track.add_note(note11)
        midi_track.add_note(note12)
        midi_track.add_note(note13)
        midi_track.add_note(note14)
        midi_track.add_note(note15)
        midi_track.add_note(note16)'''

        
        song.add_track(track1)
        song.set_time_base(time_base)
        song.output_signal = song.get_output_signal()
        song.play_song()
        song.plot_wave(10)
        song.plot_spectrum(10000)
        song.plot_phase(10000)
    




