class SynthesizerAbstract(object):
    def create_note_signal(self, note, instrument):
        raise NotImplementedError('subclasses must override synthesize_track()!')

