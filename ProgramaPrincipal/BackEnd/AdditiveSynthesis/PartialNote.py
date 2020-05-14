import numpy as np
import time

class PartialNote:
    #Clase con la que se caracteriza a cada uno de los parciales de las notas
    def __init__(self, freq, phase, start_time, d_time, d_amp, s_time, s_amp, r_time, r_amp, off_time):
        '''
        Los valores de los parametros son obtenidos de muestras de distintas señales
        freq: Frecuencia del parcial.
        phase: Fase del sample a la frecuencia del parcial.
        start_time: Tiempo en el cual comienza la nota.
        d_time: Tiempo en el que se observa el fin de la etapa de attack.
        d_amp: Amplitud alcanzada en el punto entre las etapas de attack y decay.
        s_time: Tiempo en el que se observa el fin de la etapa de decay.
        s_amp: Amplitud alcanzada en el punto entre las etapas de decay y sustain.
        r_time: Tiempo en el que se observa el fin de la etapa de sustain.
        r_amp: Amplitud alcanzada en el punto entre las etapas de sustain y release.
        off_time: Tiempo en el que se observa que la señal se anula. Fin de la etapa de release

        '''

        self.freq = freq
        self.phase = phase
        self.start_time = start_time
        self.d_time = d_time - start_time   #Tiempo desde el inicio hasta el fin de la etapa de attack.
        self.d_amp = d_amp
        self.s_time = s_time - start_time   #Tiempo desde el inicio hasta el fin de la etapa de decay.
        self.s_amp = s_amp
        self.r_time = r_time - start_time   #Tiempo desde el inicio hasta el fin de la etapa de sustain.
        self.r_amp = r_amp
        self.off_time = off_time - start_time   #Tiempo desde el inicio hasta el fin de la etapa de release.
        self.release_time = self.r_time

        self.stageAslope = self.d_amp / self.d_time #Pendiente de la etapa de attack.


        self.stageDslope = (self.s_amp - self.d_amp) / (self.s_time - self.d_time)#Pendiente de la etapa de decay.

        self.stageSslope = (self.r_amp - self.s_amp) / (self.r_time - self.s_time)#Pendiente de la etapa de sustain.


        if (self.stageSslope >= 0):
            self.stageSslope = -0.000001    

        self.stageRslope = (- self.r_amp) / (self.off_time - self.r_time)#Pendiente de la etapa de release.

        self.output_signal = np.array([])   #ADSR del parcial

        self.last_time_value = -1   #Tiempo en el cual la ADSR del parcial se hará 0.

    

    def get_phase(self):
        return self.phase

    def get_freq(self):
        return self.freq

    def __get_last_time_value__(self,note): 
        
        if (note.duration >= self.s_time):  #Si se completan las etapas de attack y decay
            if ((self.stageSslope >= 0) or  note.duration <= self.s_time - self.s_amp/self.stageSslope):    #Si pendiente de sustain es positiva o la duracion es menor que el tiempo en que la etapa s se haria 0.
                return note.duration  -((note.duration - self.s_time) * self.stageSslope + self.s_amp) / self.stageRslope   #El tiempo maximo es cuando la etapa R se hace 0.
            else:   #Si no se llega a la etapa R antes de que se anule S
                return self.s_time - self.s_amp/self.stageSslope    #Timepo maximo es cuando se anula S
        else: #Si no se completan todas las etapas...
            if note.duration <= self.d_time:
                #No hay etapa D
                return note.duration  -((note.duration ) * self.stageAslope ) / self.stageRslope
                
            elif note.duration <= self.s_time:
                #No hay etapa S
                return note.duration  -((note.duration - self.d_time) * self.stageDslope + self.d_amp) / self.stageRslope

    def get_amplitude_array(self, note):
        #Se obtiene la ADSR del parcial. Se guarda en self.output_signal

        last_time_value = self.__get_last_time_value__(note)
        self.last_time_value = last_time_value


        data = self.get_adsr(note, last_time_value)
        

        self.output_signal =  data
    
    def get_adsr(self, note, last_time_value):

        note_out = np.linspace(0, last_time_value, last_time_value*note.fs) #Arreglo de valores (depende de last_time_value)
        
        r_time_index = int(round(note.duration * note.fs)) 
     
       
        if (note.duration >= self.s_time):

            d_time_index = int(round((self.d_time) * note.fs))
            s_time_index = int(round(( self.s_time) * note.fs))
            stageA, stageD, stageS, stageR = np.split(note_out, [d_time_index, s_time_index, r_time_index]) #Se divide al arreglo de salida en las correspondientes etapas.

            #Se calculan las etapas de la ADSR.
            stageA =  (stageA ) * self.stageAslope
            stageD = (stageD  - self.d_time) * self.stageDslope + self.d_amp
            stageS = (stageS  - self.s_time) * self.stageSslope + self.s_amp
            stageR = (stageR - note.duration) * self.stageRslope + (note.duration - self.s_time) * self.stageSslope + self.s_amp
            
            data = np.concatenate([stageA, stageD, stageS, stageR]) #Se concatenan las etapas
            
        else: #Si no se completan todas las etapas...
            if note.duration <= self.d_time:    #Etapas AR
                stageA, stageR = np.split(note_out, [r_time_index])  #Se divide al arreglo de salida en las correspondientes etapas.

                #Se calculan las etapas de la ADSR.
                stageA =  (stageA ) * self.stageAslope
                stageR = (stageR  - note.duration) * self.stageRslope +note.duration * self.stageAslope
                
                data = np.concatenate([stageA, stageR]) #Se concatenan las etapas
                
                
            elif note.duration <= self.s_time:
                # ETAPAS A D Y R
                d_time_index = int(round((self.d_time) * note.fs))
        
                stageA,stageD, stageR = np.split(note_out, [d_time_index, r_time_index]) #Se divide al arreglo de salida en las correspondientes etapas.
                #Se calculan las etapas de la ADSR.
                stageA =  (stageA) * self.stageAslope
                stageD = self.d_amp + self.stageDslope * (stageD - self.d_time)
                stageR = (stageR - note.duration) * self.stageRslope + self.d_amp + ( note.duration - self.d_time) * self.stageDslope
                
                data = np.concatenate([stageA, stageD, stageR]) #Se concatenan las etapas
        
        return data

