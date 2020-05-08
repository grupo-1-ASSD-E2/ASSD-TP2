import numpy as np
import time

class PartialNote:
    def __init__(self, freq, phase, start_time, d_time, d_amp, s_time, s_amp, r_time, r_amp, off_time):
        self.freq = freq
        self.phase = phase
        self.start_time = 0
        self.d_time = d_time - start_time
        self.d_amp = d_amp
        self.s_time = s_time - start_time
        self.s_amp = s_amp
        self.r_time = r_time - start_time
        self.r_amp = r_amp
        self.off_time = off_time - start_time
        self.release_time = self.r_time

        self.stageAslope = self.d_amp / self.d_time

        self.stageDslope = (self.s_amp - self.d_amp) / (self.s_time - self.d_time)

        self.stageSslope = (self.r_amp - self.s_amp) / (self.r_time - self.s_time)

        self.stageRslope = (- self.r_amp) / (self.off_time - self.r_time)

    

    def get_phase(self):
        return self.phase

    def get_freq(self):
        return self.freq

    def __get_last_time_value__(self,note):
        
        if (note.duration > self.s_time):
            return note.ending_time  -((note.duration - self.s_time) * self.stageSslope + self.s_amp) / self.stageRslope
        else: #Si no se completan todas las etapas...
            if note.duration < self.d_time:
                return note.ending_time  -((note.duration ) * self.stageAslope ) / self.stageRslope
                
            elif note.duration < self.s_time:
                return note.ending_time  -((note.duration - self.d_time) * self.stageDslope + self.d_amp) / self.stageRslope

    def get_amplitude_array(self, note, time_base):
  
        note_on_index = time_base.get_time_index_in_time_array(note.initial_time)
        note_off_index = time_base.get_time_index_in_time_array(note.ending_time)

        last_time_value = self.__get_last_time_value__(note)

        time_array_aux = time_base.get_time_array()
        last_time_index = time_base.get_time_index_in_time_array(last_time_value)
        if (last_time_index == -1): #error
            last_time_index = note_off_index #corta al final



        zeros, time_val, zeros2 = np.split(time_array_aux, [note_on_index, last_time_index]) #se obtiene solo el arreglo que necesita

        zeros = [0] * len(zeros)
        zeros2 = [0] * len(zeros2)
        data = self.get_adsr(time_val, note, time_base)
        
        amp = np.concatenate([zeros, data, zeros2])
        return amp
    
    def get_adsr(self, time_array, note, time_base):
        
    
               
        if (note.ending_time > max(time_array)):
            r_time_index = len(time_array)-1
        else:
             r_time_index =time_base.get_time_index_in_time_subarray(time_array, note.ending_time)
       
        if (note.duration > self.s_time):
            
            d_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.d_time + note.initial_time)
            s_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.s_time + note.initial_time)
            stageA, stageD, stageS, stageR = np.split(time_array, [d_time_index, s_time_index, r_time_index])
            stageA =  (stageA - note.initial_time) * self.stageAslope
            stageD = (stageD - note.initial_time - self.d_time) * self.stageDslope + self.d_amp
            stageS = (stageS - note.initial_time - self.s_time) * self.stageSslope + self.s_amp
            stageR = (stageR - note.ending_time) * self.stageRslope + (
                           note.duration - self.s_time) * self.stageSslope + self.s_amp
            
            data = np.concatenate([stageA, stageD, stageS, stageR])
            
        else: #Si no se completan todas las etapas...
            if note.duration < self.d_time:
                stageA, stageR = np.split(time_array, [r_time_index])
                stageA =  (stageA - note.initial_time) * self.stageAslope
                stageR = (stageR  - note.ending_time) * self.stageRslope +note.duration * self.stageAslope
                
                data = np.concatenate([stageA, stageR])
                # ETAPA A y etapa R
                
            elif note.duration < self.s_time:
                # ETAPA A, ETAPA D Y ETAPA R
                d_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.d_time + note.initial_time)
        
                stageA,stageD, stageR = np.split(time_array, [d_time_index, r_time_index])
                stageA =  (stageA - note.initial_time) * self.stageAslope
                stageD = self.d_amp + self.stageDslope * (stageD - note.initial_time - self.d_time)
                stageR = (stageR - note.ending_time) * self.stageRslope + self.d_amp + (
                       note.duration - self.d_time) * self.stageDslope
                
                data = np.concatenate([stageA, stageD, stageR])
        
        return data

