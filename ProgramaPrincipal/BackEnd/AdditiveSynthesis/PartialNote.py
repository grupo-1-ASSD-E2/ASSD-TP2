import numpy as np


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

    def __get_last_time_value__(self,note_on_time,  note_off_time):
        duration = note_off_time - note_on_time
        if (duration > self.s_time):
            return note_off_time  -((note_off_time - note_on_time - self.s_time) * self.stageSslope + self.s_amp) / self.stageRslope
        else: #Si no se completan todas las etapas...
            if duration < self.d_time:
                return note_off_time  -((duration ) * self.stageAslope ) / self.stageRslope
                
            elif duration < self.s_time:
                return note_off_time  -((duration - self.d_time) * self.stageDslope + self.d_amp) / self.stageRslope

    def get_amplitude_array(self, time_array, note_on_time, note_off_time, note_on_index, note_off_index):
        
        last_time_value = self.__get_last_time_value__(note_on_time, note_off_time)

        time_array_aux = np.array(time_array)
        last_time_index = np.where(np.isclose(time_array_aux, last_time_value))[0]
        if (len(last_time_index) == 0):
            last_time_index = note_off_index
        else:
            last_time_index = last_time_index[len(last_time_index)-1]



        zeros, time_val, zeros2 = np.split(time_array_aux, [note_on_index, last_time_index])

        zeros = [0] * len(zeros)
        zeros2 = [0] * len(zeros2)
        data = self.get_adsr(time_val, note_on_time, note_off_time)
        '''
        for time in time_val:
            data.append(self.get_amplitude(time, note_on_time, note_off_time))

        
        '''
        amp = np.concatenate([zeros, data, zeros2])
        return amp
    
    def get_adsr(self, time_array, note_on_time, note_off_time):
        duration = note_off_time - note_on_time
        
        time_array = np.array(time_array)
        
        
        r_time_index = np.where(np.isclose(time_array, note_off_time, atol=1e-07))[0]
        
        
        if (note_off_time > max(time_array)):
            r_time_index = len(time_array)-1
        else:
            r_time_index = r_time_index[0]
        
        
        if (duration > self.s_time):
        
            d_time_index = np.where(np.isclose(time_array, self.d_time + note_on_time, atol=1e-05))[0][0]
            s_time_index = np.where(np.isclose(time_array, self.s_time + note_on_time, atol=1e-05))[0][0]
            stageA, stageD, stageS, stageR = np.split(time_array, [d_time_index, s_time_index, r_time_index])
            stageA =  (stageA - note_on_time) * self.stageAslope
            stageD = (stageD - note_on_time - self.d_time) * self.stageDslope + self.d_amp
            stageS = (stageS - note_on_time - self.s_time) * self.stageSslope + self.s_amp
            stageR = (stageR - note_off_time) * self.stageRslope + (
                            duration - self.s_time) * self.stageSslope + self.s_amp
            
            data = np.concatenate([stageA, stageD, stageS, stageR])
            
        else: #Si no se completan todas las etapas...
            if duration < self.d_time:
                stageA, stageR = np.split(time_array, [r_time_index])
                stageA =  (stageA - note_on_time) * self.stageAslope
                stageR = (stageR  - note_off_time) * self.stageRslope + duration * self.stageAslope
                
                data = np.concatenate([stageA, stageR])
                # ETAPA A y etapa R
                
            elif duration < self.s_time:
                # ETAPA A, ETAPA D Y ETAPA R
                d_time_index = np.where(np.isclose(time_array, self.d_time + note_on_time, atol=1e-05))[0][0]
        
                stageA,stageD, stageR = np.split(time_array, [d_time_index, r_time_index])
                stageA =  (stageA - note_on_time) * self.stageAslope
                stageD = self.d_amp + self.stageDslope * (stageD - note_on_time - self.d_time)
                stageR = (stageR - note_off_time) * self.stageRslope + self.d_amp + (
                        duration - self.d_time) * self.stageDslope
                
                data = np.concatenate([stageA, stageD, stageR])
                
        return data

