#from ProgramaPrincipal.BackEnd.TimeBase.TimeBase import TimeBase
from BackEnd.Note import Note
from BackEnd.TimeBase.TimeBase import TimeBase


#ARMAR OUTPUT SIGNAL CON EL SIZE CORRESPONDIENTE SEGUN EL TEMPO DE LA CANCION Y RELLENARO CON CEROS INICIALMENTE

class Track:
    def __init__(self):
        #self.midi_track = None
        self.notes = []
        self.instrument = None
        self.output_signal = []
        self.initial_time = 0
        self.activated = True
        self.has_changed = False
        self.velocity = 127 #Represents the volume. min: 0. max: 127.
        
    def assign_instrument(self, instrument):
        self.instrument = instrument
        self.has_changed = True


    def get_output_signal(self):
        return self.output_signal

    def add_note(self, note):
        self.notes.append(note)
        self.has_changed = True


    def set_activated(self, activated):
        if (self.activated != activated):
            self.has_changed = True
            self.activated = activated

    def toggle_track(self):
        self.activated = not self.activated
        self.has_changed = True


    def set_volume(self, volume):
        """Defines volumen of the track.
        min: 0
        max: 1 
        """
        if (0 <= volume <= 127):
            self.velocity = volume * 127
            self.has_changed = True
        else:
            return -1