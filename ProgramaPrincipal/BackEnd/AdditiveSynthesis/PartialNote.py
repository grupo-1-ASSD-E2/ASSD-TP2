import numpy as np
import time

class PartialNote:
    def __init__(self, freq, phase, start_time, d_time, d_amp, s_time, s_amp, r_time, r_amp, off_time):
        self.freq = freq
        self.phase = phase
        self.start_time = start_time
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

        self.output_signal = np.array([])

        self.last_time_value = -1

    

    def get_phase(self):
        return self.phase

    def get_freq(self):
        return self.freq

    def __get_last_time_value__(self,note): #COMPLETADO
        
        if (note.duration > self.s_time):
            return note.duration  -((note.duration - self.s_time) * self.stageSslope + self.s_amp) / self.stageRslope
        else: #Si no se completan todas las etapas...
            if note.duration < self.d_time:
                #No hay etapa D
                return note.duration  -((note.duration ) * self.stageAslope ) / self.stageRslope
                
            elif note.duration < self.s_time:
                #No hay etapa S
                return note.duration  -((note.duration - self.d_time) * self.stageDslope + self.d_amp) / self.stageRslope

    def get_amplitude_array(self, note):
    

        last_time_value = self.__get_last_time_value__(note)
        self.last_time_value = last_time_value


        data = self.get_adsr(note, last_time_value)
        

        self.output_signal =  data
    
    def get_adsr(self, note, last_time_value):

        note_out = np.linspace(0, last_time_value, last_time_value*note.fs)
        
        r_time_index = int(round(note.duration * note.fs))
     
       
        if (note.duration > self.s_time):

            d_time_index = int(round((self.d_time) * note.fs))
            s_time_index = int(round(( self.s_time) * note.fs))
            #d_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.d_time + note.initial_time)
            #s_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.s_time + note.initial_time)
            stageA, stageD, stageS, stageR = np.split(note_out, [d_time_index, s_time_index, r_time_index])
            stageA =  (stageA ) * self.stageAslope
            stageD = (stageD  - self.d_time) * self.stageDslope + self.d_amp
            stageS = (stageS  - self.s_time) * self.stageSslope + self.s_amp
            stageR = (stageR - note.duration) * self.stageRslope + (
                           note.duration - self.s_time) * self.stageSslope + self.s_amp
            
            data = np.concatenate([stageA, stageD, stageS, stageR])
            
        else: #Si no se completan todas las etapas...
            if note.duration < self.d_time:
                stageA, stageR = np.split(note_out, [r_time_index])
                stageA =  (stageA ) * self.stageAslope
                stageR = (stageR  - note.duration) * self.stageRslope +note.duration * self.stageAslope
                
                data = np.concatenate([stageA, stageR])
                # ETAPA A y etapa R
                
            elif note.duration < self.s_time:
                # ETAPA A, ETAPA D Y ETAPA R
                d_time_index = int(round((self.d_time) * note.fs))
                #d_time_index = time_base.get_time_index_in_time_subarray(time_array,  self.d_time + note.initial_time)
        
                stageA,stageD, stageR = np.split(note_out, [d_time_index, r_time_index])
                stageA =  (stageA) * self.stageAslope
                stageD = self.d_amp + self.stageDslope * (stageD - self.d_time)
                stageR = (stageR - note.duration) * self.stageRslope + self.d_amp + (
                       note.duration - self.d_time) * self.stageDslope
                
                data = np.concatenate([stageA, stageD, stageR])
        
        return data

