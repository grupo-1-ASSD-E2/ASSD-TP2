class Note:
    def __init__(self, note_number, duration, velocity, initial_time):
        self.frequency = self.__note_to_frequency__(note_number)
        self.duration = duration
        self.velocity = velocity
        self.initial_time = initial_time
        self.ending_time = initial_time + duration
        self.output_signal = [] #SINTETIZADOR TIENE QUE DEVOLVER ESTO


    @staticmethod
    def __note_to_frequency__(midi_note_code):
        a = 440  # frequency of A (coomon value is 440Hz)
        return (a / 32) * (2 ** ((midi_note_code - 9) / 12))
    
    def get_output_signal(self):
        return self.output_signal