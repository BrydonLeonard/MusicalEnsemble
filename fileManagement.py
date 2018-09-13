import glob
from music21 import converter, instrument, note, chord
import re
from numpy import array
import os


def get_training_data(folder):
    notes = []
    print('Starting import...')
    for file in glob.glob(folder + '/*.mid'):
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


def save_training_data(folder, force):
    if not os.path.exists(folder + '/notes.csv') or force:
        training_data = get_training_data(folder)
        training_data_file = open(folder + 'notes.csv', 'w')
        training_data_file.write('\n'.join(training_data))


def load_training_data(folder, force_reload_training_data):
    save_training_data(folder, force_reload_training_data)
    f = open(folder + '/notes.csv', 'r')
    data = []

    lines = f.read().split('\n')

    for l in lines:
        if l:
            trainingPattern = []
            splitLine = l.split(',')
            for item in splitLine:
                singleNote = re.sub('[()]', '', item).split(';')
                trainingPattern.append(singleNote)

            data.append(trainingPattern)

    data = array(data)
    X, y = data[:, :-1], data[:, -1]
    X.reshape(len(X), len(X[0]), len(X[0][0]))

    return X, y


def load_note_mappings(file_name):
    f = open(file_name, 'r')
    lines = [line for line in f.read().split('\n') if line]
    f.close()
    d = dict((key, value) for (value, key) in enumerate(lines))

    return d




