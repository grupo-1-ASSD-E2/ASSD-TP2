#from ProgramaPrincipal.BackEnd.TimeBase.TimeBase import TimeBase
from BackEnd.Note import Note
from BackEnd.TimeBase.TimeBase import TimeBase


#ARMAR OUTPUT SIGNAL CON EL SIZE CORRESPONDIENTE SEGUN EL TEMPO DE LA CANCION Y RELLENARO CON CEROS INICIALMENTE

class Track:
    def __init__(self):
        #self.midi_track = None
        self.notes = []
        self.instrument = None
        self.output_signal = None
        self.time_base = None #ver si esto se necesita aca o no...
        
    def assign_instrument(self, instrument):
        self.instrument = instrument

    def associate_midi_track(self, midi_track):
        self.midi_track = midi_track

    def initialize_output_signal_array(self, time_base):
        self.time_base = time_base
        self.output_signal = [0] * self.time_base.get_time_array()

    def synthesize(self): 
        for note in self.notes:
            self.instrument.synthesizer.create_note_signal(note, self.instrument)

    def get_output_signal(self):
        return self.output_signal

    def add_note(self, note):
        self.notes.append(note)
