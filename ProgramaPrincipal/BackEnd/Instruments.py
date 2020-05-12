from enum import Enum

class Instruments(Enum):
     TRUMPET = ['Trumpet', 'ProgramaPrincipal/Resources/trumpet.png']
     VIOLIN = ['Violin', 'ProgramaPrincipal/Resources/violin.png']
     OBOE = ['Oboe', 'ProgramaPrincipal/Resources/oboe.png']
     GUITAR = ['Guitar', 'ProgramaPrincipal/Resources/guitar.png']
     DRUM = ['Drum', 'ProgramaPrincipal/Resources/drum.png']
     PIANO = ['Piano', 'ProgramaPrincipal/Resources/piano.png']
     CELLO = ['Cello', 'ProgramaPrincipal/Resources/cello.png']
     VIOLA = ['Viola', 'ProgramaPrincipal/Resources/viola.png']
     MANDOLIN = ['Mandolin', 'ProgramaPrincipal/Resources/mandolin.png']
     BANJO = ['Banjo', 'ProgramaPrincipal/Resources/banjo.png']
     ACCORDEON = ['Accordeon', 'ProgramaPrincipal/Resources/accordeon.png']
     BASSOON = ['Bassoon', 'ProgramaPrincipal/Resources/bassoon.png']
     SAXOPHONE = ['Saxophone', 'ProgramaPrincipal/Resources/saxophone.png']

     @staticmethod
     def list():
        return list(map(lambda c: c.value, Instruments))

