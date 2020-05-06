class MidiNote:
    def __init__(self, midi_number, note_on_tick, velocity, note_off_tick=-1):
        self.midi_note_number = midi_number
        self.frequency = self.__midi_note_to_frequency__(midi_number)

        self.note_on_tick = note_on_tick  # in seconds
        self.note_off_tick = note_off_tick  # in seconds

        self.velocity = velocity

    def set_note_off_tick(self, note_off_tick):
        self.note_off_tick = note_off_tick

    @staticmethod
    def __midi_note_to_frequency__(midi_note_code):
        a = 440  # frequency of A (coomon value is 440Hz)
        return (a / 32) * (2 ** ((midi_note_code - 9) / 12))
