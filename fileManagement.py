import glob
from music21 import converter, instrument, note, chord


def get_training_data(folder):
    notes = []
    print('Starting import...')
    for file in glob.glob('midi/' + folder + '/*.mid'):
        print('  Importing ' + str(file))

        midi = converter.parse(file)
        notes_to_parse = None

        parts = instrument.partitionByInstrument(midi)

        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(c) for c in element.normalOrder))

    print('Import complete.')
    return notes


def load_note_mappings():
    note_mapping_file = open('notes.csv', 'r')

    d = dict()

    for line in note_mapping_file.read().split('\n'):
        spl = line.split(',')
        if (len(spl) > 1):
            d[spl[1]] = int(spl[0])

    return d
