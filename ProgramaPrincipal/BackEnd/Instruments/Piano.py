from BackEnd.SamplesBasedSynthesis.SBSynthesis import SB_Synthesizer

class Piano:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.instrument_name = 'Piano'