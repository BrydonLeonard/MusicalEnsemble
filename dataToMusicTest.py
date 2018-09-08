from music21 import note, stream
import math
notePos = dict((note, pos) for (note, pos) in [('C', 0), ('D-', 1), ('C#', 1), ('D', 2), ('E-', 3), ('D#', 3), ('E', 4), ('F', 5), ('G-', 6), ('F#', 6), ('G', 7), ('A-', 8), ('G#', 8), ('A', 9), ('B-', 10), ('A#', 10), ('B', 11), ])


def get_note_from_interval_and_offset(note1, interval, offset):
    note1_pos = notePos[note1.name] + note1.pitch.implicitOctave * 12
    note2_pos = note1_pos + interval

    note2_octave = math.floor(note2_pos / 12)

    note2_note_index = note2_pos % 12

    note2_note = 'A'

    for tup in notePos:
        if notePos[tup] == note2_note_index:
            note2_note = tup
    note2 = note.Note(note2_note + str(note2_octave))
    note2.offset = note1.offset + offset

    print(note1.pitch)
    print(note2.pitch)

    return note2


f = open('notes.csv')

l = f.readline()

spl = l.split(',')

spl[len(spl) - 1] = spl[len(spl) - 1][:-1]

notes = []

prev_note = note.Note('C4')

for i in spl:
    iSpl = i.split(';')
    iSpl[0] = iSpl[0][1:]
    iSpl[1] = iSpl[1][:-1]
    new_note = get_note_from_interval_and_offset(prev_note, float(iSpl[0]), float(iSpl[1]))
    prev_note = new_note
    notes.append(new_note)

midi_stream = stream.Stream(notes)

print(notes)

midi_stream.write('midi', fp='test_output.mid')