import numpy as np
from BackEnd.TimeBase.Tempo import Tempo

class TimeBase:
    def __init__(self, fs):
        print('Timebase created!')
        self.fs = fs
        self.tempos = [] #Tempo instances
        self.total_duration = 0     #in seconds
        self.timeline_length = 0    #number of samples 

    def add_new_tempo(self, tempo):
        self.tempos.append(tempo)
        self.total_duration += tempo.get_total_duration_of_tempo()
        new_tempo_length = int(round(self.fs * tempo.get_total_duration_of_tempo()))
        self.timeline_length += new_tempo_length 
    
    def get_total_duration(self):
        return self.total_duration

    def get_timeline_length(self):
        return self.timeline_length

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
        return self.get_time_index_in_time_array(tick_time)

    def get_time_index_in_time_array(self, time):
        time_array = self.get_time_array()
        return self.get_time_index_in_time_subarray(time_array, time)

    def get_time_index_in_time_subarray(self, time_array, time):
        time_array_index_array = np.nonzero(np.isclose(time_array, time, atol=1/(2*self.fs)))[0]
        if (len(time_array_index_array) == 0):
            return -1 #ERROR
        else:
            return time_array_index_array[0]

    # def get_min_time_between_tick(self):
    #     min_time_between_tick = 10000
    #     for tempo in self.tempos:
    #         if tempo.time_between_ticks < min_time_between_tick:
    #             min_time_between_tick = tempo.time_between_ticks
    #     return min_time_between_tick

    def get_time_array(self):
        if self.time_array is not None:
            return self.time_array
        
        




