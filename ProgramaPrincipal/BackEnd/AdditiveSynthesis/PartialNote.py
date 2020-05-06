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

    def get_amplitude(self, time, note_on_time, note_off_time):
        last_value = note_off_time  -((note_off_time - note_on_time - self.s_time) * self.stageSslope + self.s_amp) / self.stageRslope
        if note_on_time < time < last_value:
            time_aux = time - note_on_time
            duration = note_off_time - note_on_time
            if duration < self.d_time and (time_aux > duration):
                # ETAPA R
                return (time_aux - duration) * self.stageRslope + duration * self.stageAslope
            elif duration < self.s_time and time_aux > duration:
                # ETAPA R
                return (time_aux - duration) * self.stageRslope + self.d_amp + (
                        duration - self.d_time) * self.stageDslope

            elif time_aux < self.d_time:
                # ETAPA A
                return time_aux * self.stageAslope

            elif self.d_time <= time_aux < self.s_time:
                # ETAPA D
                return (time_aux - self.d_time) * self.stageDslope + self.d_amp
            elif self.s_time <= time_aux < duration:
                # ETAPA S
                return (time_aux - self.s_time) * self.stageSslope + self.s_amp
            elif duration <= time_aux < last_value:
                # ETAPA R
                return (time_aux - duration) * self.stageRslope + (
                        duration - self.s_time) * self.stageSslope + self.s_amp
            elif time_aux >= last_value:
                return 0
        else:
            return 0

    def get_phase(self):
        return self.phase

    def get_freq(self):
        return self.freq

    def get_amplitude_array(self, time_array, note_on_time, note_off_time, note_on_index, note_off_index):
        '''
        if len(time_array) > note_off_index + note_off_index * 0.4:
            zeros, time_val, zeros2 = np.split(time_array, [note_on_index, int(note_off_index * 1.4)])

        else:'''
        zeros, time_val, zeros2 = np.split(time_array, [note_on_index, len(time_array) - 1])

        zeros = [0] * len(zeros)
        zeros2 = [0] * len(zeros2)
        data = []

        for time in time_val:
            data.append(self.get_amplitude(time, note_on_time, note_off_time))

        amp = np.concatenate([zeros, data, zeros2])

        return amp
