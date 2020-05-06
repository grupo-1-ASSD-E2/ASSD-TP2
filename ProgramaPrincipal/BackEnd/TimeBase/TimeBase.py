import numpy as np
class TimeBase:
    def __init__(self,number_of_samples,  fs):
        self.number_of_samples = number_of_samples#N samples
        self.fs = fs
        self.tempos = [] #Tempo instances

    def add_new_tempo(self, tempo):
        self.tempos.append(tempo)

    def convert_tick_to_time(self, tick):
        partial_time = 0

        found_corresponding_tempo = False

        it_number = 0
        while not found_corresponding_tempo and  it_number<len(self.tempos):
            if self.tempos[it_number].end_tick < tick:
                partial_time += self.tempos[it_number].get_total_duration_of_tempo()
            else:
                found_corresponding_tempo = True
                partial_time += self.tempos[it_number].get_duration_from_tempo_start(tick)
            it_number += 1

        return partial_time

    def get_tick_index_in_time_array(self, tick):
        time_array = self.get_time_array()
        tick_time = self.convert_tick_to_time(tick)
        time_array_index = np.where(np.isclose(time_array, tick_time))[0][0]
        return time_array_index

    def get_min_time_between_tick(self):
        min_time_between_tick = 10000
        for tempo in self.tempos:
            if tempo.time_between_ticks < min_time_between_tick:
                min_time_between_tick = tempo.time_between_ticks
        return min_time_between_tick

    def get_total_duration(self):
        total_duration = 0
        for tempo in self.tempos:
            total_duration+=tempo.get_total_duration_of_tempo()
        return total_duration

    def get_time_array(self):
        return np.linspace(0, self.get_total_duration(), self.fs*self.get_total_duration())




