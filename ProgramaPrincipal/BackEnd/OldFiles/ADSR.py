import numpy as np

# Amplitude (Attack, Decay, Sustain, Release) Envelope
class ADSR:
    def __init__(self):

        self.dAttackTime = 0.10
        self.dDecayTime = 0.01
        self.dStartAmplitude = 1.0
        self.dSustainAmplitude = 0.8
        self.dReleaseTime = 0.20
        self.bNoteOn = False
        self.dTriggerOffTime = 0.0
        self.dTriggerOnTime = 0.0

    def note_on(self, d_time_on):  # Call when key is pressed
        self.dTriggerOnTime = d_time_on
        self.bNoteOn = True;

    def note_off(self, dTimeOff):  # Call when key is released

        self.dTriggerOffTime = dTimeOff;
        #self.bNoteOn = False

    def get_amplitude(self, dTime):  # Get the correct amplitude at the requested point in time

        dAmplitude = 0.0;
        dLifeTime = dTime - self.dTriggerOnTime

        if self.bNoteOn:

            if 0 <= dLifeTime <= self.dAttackTime:
                # In attack Phase - approach max amplitude
                dAmplitude = (dLifeTime / self.dAttackTime) * self.dStartAmplitude

            if self.dAttackTime < dLifeTime <= (self.dAttackTime + self.dDecayTime):
                # In decay phase - reduce to sustained amplitude
                dAmplitude = ((dLifeTime - self.dAttackTime) / self.dDecayTime) * (
                        self.dSustainAmplitude - self.dStartAmplitude) + self.dStartAmplitude;

            if dLifeTime > (self.dAttackTime + self.dDecayTime):
                # In sustain phase - dont change until note released
                dAmplitude = self.dSustainAmplitude

        else:

            # Note has been released, so in release phase
            dAmplitude = ((dTime - self.dTriggerOffTime) / self.dReleaseTime) * (
                    0.0 - self.dSustainAmplitude) + self.dSustainAmplitude

        # Amplitude should not be negative

        for i in range (0, len(dAmplitude)):
            if dAmplitude[i] <= 0.0001:
                dAmplitude[i] = 0.0
        # Convert to 16-bit data
        dAmplitude = dAmplitude.astype(np.int16)

        return dAmplitude;
