from enum import Enum

class Instruments(Enum):
     TRUMPET = ['Trumpet', 'instruments/assets/instruments/trumpet.png']
     VIOLIN = ['Violin', 'instruments/assets/instruments/violin.png']
     OBOE = ['Oboe', 'instruments/assets/instruments/oboe.png']
     GUITAR = ['Guitar', 'instruments/assets/instruments/guitar.png']
     DRUM = ['Drum', 'instruments/assets/instruments/drum.png']
     PIANO = ['Piano', 'instruments/assets/instruments/piano.png']
     CELLO = ['Cello', 'instruments/assets/instruments/cello.png']
     VIOLA = ['Viola', 'instruments/assets/instruments/viola.png']
     MANDOLIN = ['Mandolin', 'instruments/assets/instruments/mandolin.png']
     BANJO = ['Banjo', 'instruments/assets/instruments/banjo.png']
     ACCORDEON = ['Accordeon', 'instruments/assets/instruments/accordeon.png']
     BASSOON = ['Bassoon', 'instruments/assets/instruments/bassoon.png']
     SAXOPHONE = ['Saxophone', 'instruments/assets/instruments/saxophone.png']

     @staticmethod
     def list():
        return list(map(lambda c: c.value, Instruments))

