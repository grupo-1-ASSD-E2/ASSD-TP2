from enum import Enum
from BackEnd.AudioEfects.Flanger.Flanger import Flanger
from BackEnd.AudioEfects.Flanger.Vibrato import Vibrato
from BackEnd.AudioEfects.Reverberation.Reverb import Reverb
from BackEnd.AudioEfects.Reverberation.LowPassReverb import LowPassReverb
from BackEnd.AudioEfects.Reverberation.AllPassReverb import AllPassReverb
from BackEnd.AudioEfects.Reverberation.PlainPeverb import PlainReverb
from BackEnd.AudioEfects.Reverberation.Eco import EcoSimple


class Effects(Enum):
    VIBRATO = ['Vibrato', Vibrato.default_properties, Vibrato]
    FLANGER = ['Flanger', Flanger.default_properties, Flanger]
    ECO = ['Eco', EcoSimple.default_properties, EcoSimple]
    REVERB = ['Reverb', Reverb.default_properties, Reverb]
    REVERBLP = ['Reverb pasa-bajos', LowPassReverb.default_properties, Reverb]
    REVERBAP = ['Reverb pata-todo', AllPassReverb.default_properties, AllPassReverb]
    PLAINREVERB = ['Reverb plano', PlainReverb.default_properties, PlainReverb]

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Effects))

