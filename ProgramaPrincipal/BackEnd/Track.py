
from BackEnd.TimeBase.TimeBase import TimeBase

#from ProgramaPrincipal.BackEnd.TimeBase.TimeBase import TimeBase
from TimeBase.TimeBase import TimeBase



class Track:
    def __init__(self):
        self.midi_track = None
        self.instrument = None
        self.output_signal = None
        self.time_base = None

    def assign_instrument(self, instrument):
        self.instrument = instrument

    def associate_midi_track(self, midi_track):
        self.midi_track = midi_track

    def initialize_output_signal_array(self, time_base):
        self.time_base = time_base
        self.output_signal = [0] * self.time_base.get_time_array()

    def synthesize(self):
        self.instrument.synthesizer.synthesize_track(self)

    def get_output_signal(self):
        return self.output_signal
