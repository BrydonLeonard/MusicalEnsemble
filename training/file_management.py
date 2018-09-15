import glob
from music21 import converter, instrument, note, chord
import re
from numpy import array
import os


def load_note_mappings():
    note_mapping_file = open('notes.csv', 'r')

    d = dict()

    for line in note_mapping_file.read().split('\n'):
        spl = line.split(',')
        if (len(spl) > 1):
            d[spl[1]] = int(spl[0])

    return d


def load_training_data(folder, genre):
    file_name = glob.glob(folder + '/*' + genre + '*.csv')[0]
    with open(file_name, 'r') as f:
        data = [line.split(',') for line in f.read().split('\n')]

    data = array(data)
    x, y = data[:, :-1], data[:, -1]
    x.reshape(len(x), len(x[0]), len(x[0][0]))

    return x, y


def load_note_mappings(file_name):
    with open(file_name, 'r') as f:
        lines = [line for line in f.read().split('\n') if line]
    d = dict((key, value) for (value, key) in enumerate(lines))

    return d




