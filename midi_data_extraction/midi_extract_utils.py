import math
from music21 import converter, instrument, note, chord

sequenceLength = 100 + 1
notePos = dict((note, pos) for (note, pos) in [('C', 0), ('D-', 1), ('C#', 1), ('D', 2), ('E-', 3), ('D#', 3), ('E', 4), ('F', 5), ('G-', 6), ('F#', 6), ('G', 7), ('A-', 8), ('G#', 8), ('A', 9), ('B-', 10), ('A#', 10), ('B', 11), ])


def get_interval_size(note1, note2, clamp_range):
    global notePos
    note1Pos = notePos[note1.name] + note1.pitch.implicitOctave * 12
    note2Pos = notePos[note2.name] + note2.pitch.implicitOctave * 12

    diff = note2Pos - note1Pos

    if diff < clamp_range[0]:
        diff = diff % clamp_range[0]
    elif diff > clamp_range[1]:
        diff = diff % clamp_range[1]
    return diff


def add_interval_to_list(l, prev_note, note):
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


def make_training_data_from_sequence(sequence):
    ret_training_data = []
    for i in range(sequenceLength, len(sequence)):
        ret_training_data.append(sequence[i - sequenceLength:i])
    return ret_training_data


def extract_sequence_from_midi_file(file):
    notes_to_parse = None
    try:
        midi = converter.parse(file)
        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes

        prev_note = None
        note_sequence = []

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                note_sequence, prev_note = add_interval_to_list(note_sequence, prev_note, element)
            elif isinstance(element, chord.Chord):
                chordNotes = element.pitchNames
                firstChordNote = note.Note(chordNotes[0] + str(prev_note.pitch.implicitOctave))
                for n in chordNotes:
                    if prev_note is not None:
                        n = note.Note(n + str(prev_note.pitch.implicitOctave))
                    else:
                        n = note.Note(n)
                    n.offset = element.offset
                    note_sequence, prev_note = add_interval_to_list(note_sequence, prev_note, n)
                note_sequence, prev_note = add_interval_to_list(note_sequence, prev_note, firstChordNote)

        return note_sequence
    except:
        print('    Import failed.')
        return []

