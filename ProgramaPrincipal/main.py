from mido import MidiFile

mid = MidiFile('Resources/Rodrigo_-_2do_movimiento_Concierto_de_Aranjuez__Adagio.mid', clip=True)
mid1 = MidiFile('Resources/Movie_Themes_-_Star_Wars_-_by_John_Willams.mid', clip=True)
mid2 = MidiFile('Resources/Movie_Themes_-_Toy_Story.mid', clip=True)


#type 0 (single track): all messages are saved in one track
#type 1 (synchronous): all tracks start at the same time
#type 2 (asynchronous): each track is independent of the others
print(mid)
for track in mid.tracks:
    print(track)

for track in mid.tracks:
    print(track)
    for msg in track:
        print(msg)
