from training import file_management
import math
from music21 import note

notePos = dict((note, pos) for (note, pos) in [('C', 0), ('D-', 1), ('C#', 1), ('D', 2), ('E-', 3), ('D#', 3), ('E', 4), ('F', 5), ('G-', 6), ('F#', 6), ('G', 7), ('A-', 8), ('G#', 8), ('A', 9), ('B-', 10), ('A#', 10), ('B', 11), ])
mappings = file_management.load_note_mappings('note_mappings.csv')


def note_to_category(note, length):
    length_string = ''
    if float(length) % 1 == 0:
        length_string = "%.0f" % float(length)
    else:
        length_string = "%.1f" % float(length)
    note = ("%.0f" % float(note)) + ';' + length_string

    return mappings[note]


def category_to_note_and_offset(category):
    for k in mappings:
        if mappings[k] == category:
            spl = k.split(';')
            return spl[0], spl[1]


def get_note_from_interval_and_offset(note1, interval, offset):
    note1_pos = notePos[note1.name]
    note2_pos = (note1_pos + int(interval)) % 12

    #note2_note = 'A'

    for tup in notePos:
        if notePos[tup] == note2_pos:
            note2_note = tup

    note2_octave = note1.pitch.implicitOctave

    if note1_pos < note2_pos and int(interval) < 0:
        note2_octave -= 1
    elif note1_pos > note2_pos and int(interval) > 0:
        note2_octave += 1

    note2_octave = max(0, note2_octave)

    note2 = note.Note(nameWithOctave=(note2_note + str(note2_octave)))
    note2.offset = note1.offset + float(offset)

    return note2
