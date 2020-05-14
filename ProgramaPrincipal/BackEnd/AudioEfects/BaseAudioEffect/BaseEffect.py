# Audio effect base class
import numpy as np


class Effect(object):
    def __init__(self, name):
        self.name = name
        self.properties = {}  # {"Prop. Name": ((data_type, (min, max)), default_value)} requested format

    def get_attributes(self):
        """ Provide basic attributes to adjust for gui implementation """
        return self.properties.copy()

    def compute(self, audio_input: np.ndarray):
        pass

    def get_impulse_response(self) -> np.ndarray:
        pass

    def change_param(self, new_properties):
        pass
