class Track:
    def __init__(self, time_array):
        self.notes = []
        self.instrument_assigned = None
        self.time_array = time_array
        self.out_signal = []

    def add_note(self, note):
        if self.instrument_assigned is not None:
            note.assing_instrument(self.instrument_assigned)
        self.notes.append(note)

    def assign_instrument(self, instrument):
        self.instrument_assigned = instrument
        for note in self.notes:
            note.assing_instrument(instrument)

    def create_out_signal(self):
        for i in range(0, len(self.notes)):
            if i == 0:
                self.out_signal = self.notes[i].y_values
            else:
                self.out_signal += self.notes[i].y_values

