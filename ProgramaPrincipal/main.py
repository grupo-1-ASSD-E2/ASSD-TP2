from mido import MidiFile

mid = MidiFile('Resources/Movie_Themes_-_Toy_Story.mid', clip=True)
print(mid)
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

