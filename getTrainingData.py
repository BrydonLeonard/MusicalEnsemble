import glob
from music21 import converter, instrument, note, chord
import math
from numpy import array
notePos = dict((note, pos) for (note, pos) in [('C', 0), ('D-', 1), ('C#', 1), ('D', 2), ('E-', 3), ('D#', 3), ('E', 4), ('F', 5), ('G-', 6), ('F#', 6), ('G', 7), ('A-', 8), ('G#', 8), ('A', 9), ('B-', 10), ('A#', 10), ('B', 11), ])

note_sequence = []

def get_interval_size(note1, note2, clampRange):
    global notePos
    note1Pos = notePos[note1.name] + note1.pitch.implicitOctave * 12
    note2Pos = notePos[note2.name] + note2.pitch.implicitOctave * 12

    diff = note2Pos - note1Pos

    if diff < clampRange[0]:
        diff = diff % clampRange[0]
    elif diff > clampRange[1]:
        diff = diff % clampRange[1]
    return diff


def add_interval_to_list(l, prev_note, note):
    interval_size = 0
    offset = 0
    if prev_note is not None:
        interval_size = get_interval_size(prev_note, note, (-12, 12))
        if note.offset < prev_note.offset:
            offset = 1
        else:
            offset = note.offset - prev_note.offset
    else:
        interval_size = get_interval_size(note, note, (-12, 12))

    offset = min(math.ceil(offset * 2) % 2, 1.5)

    l.append((interval_size, offset))

    return l, note


print('Importing midi files...')
for file in glob.glob('midi\\testMidiFolder\\*.mid'):
    print('  Importing ' + str(file))

    print('_'.join(file.split('\\')[:-1]) + '.txt')

    notesToParse = None

    midi = converter.parse(file)

    parts = instrument.partitionByInstrument(midi)

    if parts:
        notesToParse = parts.parts[0].recurse()
    else:
        notesToParse = midi.flat.notes

    prev_note = None

    for element in notesToParse:
        if isinstance(element, note.Note):
            note_sequence, prev_note = add_interval_to_list(note_sequence, prev_note, element)
        elif isinstance(element, chord.Chord):
            chordNotes = element.pitchNames
            for n in chordNotes:
                if prev_note is not None:
                    n = note.Note(n + str(prev_note.pitch.implicitOctave))
                else:
                    n = note.Note(n)
                n.offset = element.offset
                note_sequence, prev_note = add_interval_to_list(note_sequence, prev_note, n)

sequenceLength = 100 + 1

training_patterns = []

print('Import complete.')

print('Creating training data...')
for i in range(sequenceLength, len(note_sequence)):
    training_patterns.append(note_sequence[i - sequenceLength:i])

training_patterns = array(training_patterns)

print('Created ' + str(len(training_patterns)) + ' training patterns')

outFile = open('notes.csv', 'w')

print('Writing training data...')
for p in training_patterns:
    outFile.write(','.join(['(' + ';'.join([str(k) for k in j]) + ')' for j in p]) + '\n')

print('Training data written.')
