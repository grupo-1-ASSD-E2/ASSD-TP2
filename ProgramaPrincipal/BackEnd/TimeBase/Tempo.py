class Tempo:
    def __init__(self, time_between_ticks, start_tick, end_tick):
        self.time_between_ticks = time_between_ticks #in seconds
        self.start_tick = start_tick
        self.end_tick = end_tick


    def get_total_duration_of_tempo(self):
        return self.time_between_ticks * (self.end_tick-self.start_tick)

    def get_duration_from_tempo_start(self, tick):
        return self.time_between_ticks * (tick - self.start_tick)