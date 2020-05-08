class Tempo:
    def __init__(self, tempo, ticks_per_beat, delta_ticks, start_tick):
        print('New tempo!')
        self.tempo = tempo
        self.ticks_per_beat = ticks_per_beat
        self.delta_ticks = delta_ticks
        self.start_tick = start_tick
        self.end_tick = start_tick + delta_ticks
        self.seconds_per_tick = int((self.tempo / self.ticks_per_beat) * 1000000) #self.__get_seconds_per_tick__(self.tempo, self.ticks_per_beat)
        self.total_duration_of_tempo = self.seconds_per_tick * self.delta_ticks #duration in seconds!!
        print('total duration of tempo:', self.total_duration_of_tempo)

    def get_total_duration_of_tempo(self):
        return self.total_duration_of_tempo

    def get_duration_from_tempo_start(self, tick):
        return self.seconds_per_tick * (tick - self.start_tick)