from BackEnd.SynthesizerAbstract import SynthesizerAbstract
import numpy as np
import time
from BackEnd.AdditiveSynthesis.PartialNote import PartialNote
from BackEnd.Note import Note
import sounddevice as sd
from BackEnd.Instruments import Instruments
import matplotlib.pyplot as plt

class AdditiveSynthesizer(SynthesizerAbstract):
    def __init__(self):
        i = 0

    def create_note_signal(self, note, instrument):
        #Crear la señal de salida de la nota que ingrese como parametro

        amplitude_array = None
        
        partials = self.__get_partials__(instrument, note.frequency)    #Se buscan los parciales del instrumento indicado
        for i in range(0, len(partials)):
            freq = partials[i].get_freq()
            phase = partials[i].get_phase()
           
            partials[i].get_amplitude_array(note)   #Se obtiene la ADSR de los parciales            
            
            time_vals = np.linspace(0, partials[i].last_time_value, int(note.fs*partials[i].last_time_value))    #Se crea el arreglo de tiempo para la señal

            output_sine = partials[i].output_signal * np.sin(freq * 2 * np.pi * time_vals - 180*phase/np.pi )   #Se multiplica la ADSR con el seno de cada parcial

            #Se suman las señakes de cada parcial
            if i == 0:
                amplitude_array = output_sine
            else:
                difference = len(amplitude_array) - len(output_sine)    #Chequea diferencias de longitudes para poder sumar
                zeros = np.zeros(abs(difference))                       #Crea un arreglo de ceros que permita igualar las longitudes
                if (difference > 0):    #Dependiendo de cual sea mas grande, el arreglo de ceros se concatena a uno u otros

                    amplitude_array += np.concatenate([output_sine, zeros]) #Se concatena y se suma
                elif (difference <0):
                    amplitude_array = np.concatenate([amplitude_array, zeros]) +output_sine
                else:
                    amplitude_array += output_sine


        note.output_signal =   amplitude_array    #Se obtuvo la señal de salida de la nota  

    def __get_partials__(self, instrument, frequency):
        #Funcion para obtener los parciales de un instrumento a una frecuencia indicada.
        #Se devuelve un arreglo de objetos de la clase PartialNote.
        #Los parametros de cada parcial fueron obtenidos a partir del analisis de distintos samples de los instrumentos


        
        if (instrument == Instruments.TRUMPET.value[0]):

            if frequency <= 500:    #Se obtuvo una serie de datos por debajo de 500Hz y otra por encima de 500Hz para aumentar precisión debido a la ley de caída de los parciales.
                freq_of_samples = 261.63    #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.
                partial1 = PartialNote(261.65532 * multiplier, 0.76483, 0.37, 0.4728, 0.0365, 0.91, 0.0291, 7.4, 0.028, 7.61)
            
                partial2 = PartialNote(523.310642 * multiplier, 0.1167782, 0.37, 0.46, 0.06, 2.58, 0.058, 7.4, 0.05, 7.6)

                partial3 = PartialNote(784.837889 * multiplier, -1.5167848, 0.37, 0.4728, 0.11, 2.6367, 0.0978, 7.4, 0.084,
                                    7.57)

                partial4 = PartialNote(1046.6212841 * multiplier, 1.4703592579, 0.37, 0.84, 0.165, 2.71, 0.1336, 7.4, 0.1124,
                                    7.54)

                partial5 = PartialNote(1308.2766 * multiplier, 1.646486, 0.37, 0.748, 0.104565, 2.714, 0.06745, 7.4, 0.05, 7.52)

                partial6 = PartialNote(1569.803852 * multiplier, -0.554181, 0.37, 0.73668, 0.1596, 2.49, 0.126, 7.4, 0.1, 7.55)

                partial7 = PartialNote(1831.45917 * multiplier, -0.14542, 0.37, 0.786876, 0.098, 2.75693, 0.075, 7.4, 0.065, 7.5)

                partial8 = PartialNote(2093.8829 * multiplier, -2.553459, 0.37, 0.786876, 0.0916, 2.5938, 0.05613, 7.4, 0.04, 7.5)

                partial9 = PartialNote(2355.92248 * multiplier, 1.5498516, 0.37, 0.786876, 0.058, 2.9075, 0.041, 7.4, 0.03166,
                                    7.52)

                partial10 = PartialNote(2617.5778 * multiplier, -2.80477, 0.37, 0.8245, 0.0688, 2.94515, 0.045785, 7.4, 0.0343, 7.51)

                partial11 = PartialNote(2879.7454 * multiplier, 2.781639, 0.37, 0.8157, 0.08, 3.2, 0.0425, 7.4, 0.03, 7.5)

                partial12 = PartialNote(3141.4007 * multiplier, 1.441315, 0.37, 0.8157, 0.0543, 3.33, 0.017, 7.4, 0.014, 7.5)

                partial13 = PartialNote(3403.184136 * multiplier, -1.84469,0.37, 0.8284, 0.038, 2.977, 0.0136, 7.4, 0.01, 7.49)

                partial14 = PartialNote(3661.50953 * multiplier, 1.0291, 0.37, 0.803, 0.0254, 2.774, 0.0097, 7.4, 0.0063, 7.5)

                partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial7, partial8, partial9, partial10,
                            partial11, partial12, partial13, partial14]
                
                return partials
            else:
                freq_of_samples = 783.99 #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.
                partial1 = PartialNote(784.52889 * multiplier,-2.0838746, 0.37, 0.57, 0.2708, 1.21671, 0.240596, 5.8, 0.203, 6.1)

                partial2 = PartialNote( 1566.24305 * multiplier,-2.614516, 0.37, 0.708, 0.4335, 1.47095, 0.325361, 5.7, 0.32536, 6.1)

                partial3 = PartialNote(2354.3685 * multiplier,-1.772421, 0.37, 0.676458, 0.16827, 1.4074, 0.120688, 5.7, 0.073, 6.05)

                partial4 = PartialNote(3141.243 * multiplier,1.34737, 0.37, 0.856542, 0.0893, 2.53026, 0.041663, 5.7, 0.0216, 6.05)


                partial5 = PartialNote(3925.77194 * multiplier,1.455032, 0.37, 0.8565, 0.049, 2.39255, 0.0253, 5.7, 0.014, 6.05)

                partials = [partial1, partial2, partial3, partial4, partial5]
                return partials

        elif(instrument == Instruments.OBOE.value[0]):

            if (frequency <=500):#Se obtuvo una serie de datos por debajo de 500Hz y otra por encima de 500Hz para aumentar precisión debido a la ley de caída de los parciales.
                freq_of_samples = 261.63     #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.
                partial1 = PartialNote(260.9281 * multiplier,-1.83709, 0, 0.1168, 0.132, 0.296, 0.128, 6.36, 0.124, 6.75)

                partial2 = PartialNote(521.712996 * multiplier,-1.43441, 0, 0.07, 0.07, 0.442, 0.07, 6.36, 0.07, 6.75)

                partial3 = PartialNote(782.641099 * multiplier,-1.3449376, 0, 0.139, 0.0987, 0.307, 0.0957, 6.36, 0.08, 6.77)

                partial4 = PartialNote(1043.13957 * multiplier,2.83307, 0, 0.15, 0.163, 0.35, 0.178, 6.36, 0.153, 6.78)

                partial5 = PartialNote(1304.0677 * multiplier,2.82392, 0, 0.117, 0.41, 0.42, 0.4, 6.36, 0.36, 6.7)

                partial6 = PartialNote(1564.85257 * multiplier,-2.6445677, 0, 0.103, 0.307, 0.24, 0.297, 6.36, 0.216, 6.7)

                partial7 = PartialNote(1825.92388 * multiplier,-1.5581, 0, 0.092, 0.2, 0.43, 0.2, 6.36, 0.2, 6.7)

                partial8 = PartialNote(2086.85198 * multiplier,-1.8931935, 0, 0.137, 0.0857, 0.375, 0.089, 6.36, 0.0688, 6.76)


                partial9 = PartialNote(2347.78 * multiplier,2.433, 0, 0.103, 0.013, 0.6, 0.019, 6.36, 0.019, 6.75)


                
                partials = [partial1, partial2, partial3,partial4, partial5, partial6, partial8, partial9]
                return partials
            else:
                freq_of_samples = 932.328 #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.

                partial1 = PartialNote(928.7298 * multiplier,0.01449, 0, 0.112829, 0.520753, 1.45245, 0.4917, 5.7, 0.4626, 6.67)

                partial2 = PartialNote( 1861.089727 * multiplier,0.75277, 0, 0.191, 0.472, 1.2515, 0.51671, 5.7, 0.5167, 6.65)

                partial3 = PartialNote(2786.47982 * multiplier,-1.87667, 0, 0.113, 0.0815, 0.961257, 0.117, 5.7, 0.129, 6.65)

                partials = [partial1, partial2, partial3]
                return partials


        elif (instrument == Instruments.VIOLIN.value[0]):

            if frequency <= 500:#Se obtuvo una serie de datos por debajo de 500Hz y otra por encima de 500Hz para aumentar precisión debido a la ley de caída de los parciales.
                freq_of_samples = 261.63    # Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.
                partial1 = PartialNote(261.58854 * multiplier, -2.93465, 0.026, 0.5, 0.35, 0.569, 0.2837, 3, 0.2837, 3.489)

                partial2 = PartialNote(522.94078 * multiplier, 2.7098, 0.026, 0.453, 0.091, 0.523, 0.11, 3, 0.09, 3.27575)

                partial3 = PartialNote(784.52932 * multiplier, 0.363645, 0.026, 0.0713, 0.0594, 0.546, 0.1496, 3, 0.1307, 3.29)

                partial4 = PartialNote(1039.73765 * multiplier, 2.1862, 0.026, 0.03234, 0.0376, 0.54, 0.07, 3, 0.0495, 3.3)

                partial5 = PartialNote(1314.3229 * multiplier, 1.46007, 0.026, 0.0488, 0.0388, 0.724, 0.12, 3, 0.1, 3.3)

                partial6 = PartialNote(1580.4012 * multiplier, 1.971578, 0.026, 0.297, 0.029, 0.53, 0.107, 3, 0.077, 3.3)

                partial7 = PartialNote(1841.98978 * multiplier, -0.59578, 0.026, 0.05, 0.024, 0.56, 0.05, 3, 0.0425, 3.3)

                partial8 = PartialNote(2091.054205 * multiplier, 3.101057, 0.026, 0.05238, 0.02, 0.59, 0.07, 3, 0.069, 3.3)

                partial9 = PartialNote(2589.18306 * multiplier,0.03179217, 0.026, 0.058, 0.0236, 0.61, 0.06, 3, 0.06, 3.3)

                partials = [partial1, partial2, partial3, partial4, partial5, partial6, partial7, partial8, partial9]
                
                return partials

            else:
                freq_of_samples = 932.33 #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.

                partial1 = PartialNote(932.633 * multiplier,2.89414, 0, 0.4247, 0.5271, 0.7276, 0.433716, 6.4, 0.418, 6.658)
                
                partial2 = PartialNote(1870.971 * multiplier, -0.46688, 0, 0.4, 0.284, 0.5257, 0.2584, 6.4, 0.2236, 6.66)
                                
                partial3 = PartialNote(2808.8025 * multiplier, -2.896195, 0, 0.374, 0.249, 0.488, 0.227, 6.4, 0.1985, 6.63)
                                
                partial4 = PartialNote( 3749.423 * multiplier, -1.21915, 0, 0.387, 0.365, 0.5, 0.29, 6.4, 0.265, 6.61)

                partial5 = PartialNote(4682.183 * multiplier, 1.835926, 0, 0.7907, 0.1234, 0.98, 0.1, 6.4, 0.085, 6.61)

                partial6 = PartialNote(5577.1605 * multiplier, -2.34273, 0, 0.4105, 0.0616, 0.6, 0.05, 6.4, 0.045, 6.637)

                partials = [partial1, partial2, partial3, partial4, partial5, partial6]

                return partials



        elif (instrument == Instruments.ACCORDEON.value[0]):

            if frequency<=500:#Se obtuvo una serie de datos por debajo de 500Hz y otra por encima de 500Hz para aumentar precisión debido a la ley de caída de los parciales.

                freq_of_samples = 261.63    #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples    #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.

                partial1 = PartialNote(262.3775 * multiplier, 2.151939, 0.01, 0.114, 0.3647, 0.192, 0.339, 3.93, 0.3124, 4.119)
                
                
                partial2 = PartialNote(524.755 * multiplier, 0.1374, 0.01, 0.146, 0.379, 0.264, 0.345, 3.93, 0.218, 4.06)
                
                partial3 = PartialNote(787.13263 * multiplier, -0.2871, 0.01, 0.298656, 0.706515, 0.51749, 0.671, 3.93, 0.511, 4.07)
                
                partial4 = PartialNote(1049.35665 * multiplier, 1.305462, 0.01, 0.0666, 0.205, 0.156, 0.0753, 3.93, 0.0623, 4.08)

                partial5 = PartialNote(1311.7342 * multiplier, 1.722816, 0.01, 0.085, 0.308, 0.286, 0.2635, 3.93, 0.2, 4)

                partial6 = PartialNote(1574.112 * multiplier, -1.35669, 0.01, 0.156, 0.147, 0.3, 0.1287, 3.93, 0.101, 4.08)

                partial8 = PartialNote(2099.02 * multiplier, -2.73082, 0.01, 0.184, 0.036, 0.513, 0.0283, 3.93, 0.017, 4.033)

                partial9 = PartialNote(2361.397896 * multiplier, 1.916575, 0.01, 0.139, 0.051, 0.5843, 0.0371, 3.93, 0.0449, 4.055)

                partial14 = PartialNote(3673.132 * multiplier, -0.82067, 0.01, 0.128, 0.039, 0.254, 0.0339, 3.93, 0.028, 4.06)

                partial15 = PartialNote(3935.5096 * multiplier, -0.02447, 0.01, 0.108, 0.055, 0.32, 0.0486, 3.93, 0.0486, 4.06)

                partial16 = PartialNote(4197.887177 * multiplier, 1.5649835, 0.01, 0.183, 0.044, 0.39, 0.039, 3.93, 0.03, 4.046)

                partial17 = PartialNote(4460.26472 * multiplier, 2.4423946, 0.01, 0.1635, 0.06, 0.29, 0.059, 3.93, 0.049, 4.02)

                partials = [partial1, partial2,partial3, partial4, partial5, partial6, partial8, partial9, partial14, partial15, partial16, partial17]
             
                return partials
            else:
                freq_of_samples = 783.99 #Frecuencia con la que se obtuvieron los datos

                multiplier = frequency / freq_of_samples #Multiplicador de frecuencia que permite shiftear los datos a la frecuencia buscada.

                partial1 = PartialNote(787.56725 * multiplier,0.15037, 0.01, 0.057, 0.445765, 0.4056, 0.47356, 3.5, 0.432, 3.71)
                
                partial2 = PartialNote(1575.1345 * multiplier, -2.074696, 0.01, 0.03476, 0.12447, 0.1022, 0.06965, 3.5, 0.055, 3.653)
                                
                partial3 = PartialNote(2362.70176 * multiplier, 2.7943527, 0.01, 0.0797, 0.692263, 0.5404, 0.6713, 3.5, 0.5875, 3.653)
                                
                partial4 = PartialNote( 3150.26901 * multiplier, -0.598855, 0.01, 0.046, 0.092, 1.04606, 0.0836, 3.5, 0.0474, 3.63)

                partial5 = PartialNote(3937.83627 * multiplier, 0.499567, 0.01, 0.06847, 0.1195, 0.3494, 0.116, 3.5, 0.1093, 3.62)

                partial6 = PartialNote(4725.40352 * multiplier, -2.542502, 0.01, 0.05985, 0.0864, 0.215488, 0.08184, 3.5, 0.079553, 3.64)

                partials = [partial1, partial2, partial3, partial4, partial5, partial6]

                return partials
