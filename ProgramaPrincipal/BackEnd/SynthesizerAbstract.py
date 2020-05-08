class SynthesizerAbstract(object):
    def create_note_signal(self, note, time_base, instrument):
        raise NotImplementedError('subclasses must override synthesize_track()!')

