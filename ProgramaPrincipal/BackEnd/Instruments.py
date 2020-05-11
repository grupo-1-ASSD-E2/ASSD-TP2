from enum import Enum

class Instruments(Enum):
     TRUMPET = ['Trumpet', 'ProgramaPrincipal/Resources/trumpet']
     VIOLIN = ['Violin', 'ProgramaPrincipal/Resources/violin']
     OBOE = ['Oboe', 'ProgramaPrincipal/Resources/oboe']
     GUITAR = ['Guitar', 'ProgramaPrincipal/Resources/guitar']
     DRUM = ['Drum', 'ProgramaPrincipal/Resources/drum']
     PIANO = ['Piano', 'ProgramaPrincipal/Resources/piano']
     CELLO = ['Cello', 'ProgramaPrincipal/Resources/cello']
     VIOLA = ['Viola', 'ProgramaPrincipal/Resources/viola']
     MANDOLIN = ['Mandolin', 'ProgramaPrincipal/Resources/mandolin']
     BANJO = ['Banjo', 'ProgramaPrincipal/Resources/banjo']
     ACCORDEON = ['Accordeon', 'ProgramaPrincipal/Resources/accordeon']
     BASSOON = ['Bassoon', 'ProgramaPrincipal/Resources/bassoon']
     SAXOPHONE = ['Saxophone', 'ProgramaPrincipal/Resources/saxophone']

     @staticmethod
     def list():
        return list(map(lambda c: c.value, Instruments))

