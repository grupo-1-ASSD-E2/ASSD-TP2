class Tempo:
    def __init__(self, tempo, ticks_per_beat, delta_ticks, start_tick):
        #print('New tempo!')
        self.tempo = tempo
        self.ticks_per_beat = ticks_per_beat
        self.delta_ticks = delta_ticks
        self.start_tick = start_tick
        #self.end_tick = start_tick + delta_ticks
        self.end_tick = start_tick + delta_ticks - 1
        self.seconds_per_tick = (self.tempo / self.ticks_per_beat) * 10**-6 #self.__get_seconds_per_tick__(self.tempo, self.ticks_per_beat)
        #self.total_duration_of_tempo = self.seconds_per_tick * self.delta_ticks #duration in seconds!!
        self.total_duration_of_tempo = self.seconds_per_tick * (self.delta_ticks - 1) #duration in seconds!!
        print('start_tick', self.start_tick)
        print('end tick', self.end_tick)
        print('total duration of tempo:', self.total_duration_of_tempo)

    def get_total_duration_of_tempo(self):
        return self.total_duration_of_tempo

    def get_duration_from_tempo_start(self, tick):
        return self.seconds_per_tick * (tick - self.start_tick)