import glob
from numpy import array
import numpy as np


def load_note_mappings():
    note_mapping_file = open('notes.csv', 'r')

    d = dict()

    for line in note_mapping_file.read().split('\n'):
        spl = line.split(',')
        if len(spl) > 1:
            d[spl[1]] = int(spl[0])

    return d


def load_training_data(folder, genre):
    file_name = glob.glob(folder + '/*' + genre + '*.csv')[0]
    with open(file_name, 'r') as f:
        data = array([])
        output = array([])
        for line in f:
            line = line.rstrip()
            if line:
                spl = line.split(',')
                np.append(data, spl[:-1])
                np.append(output, spl[-1])

    return data.reshape(len(data), 100, 1), output


def load_note_mappings(file_name):
    with open(file_name, 'r') as f:
        lines = [line for line in f.read().split('\n') if line]
    d = dict((key, value) for (value, key) in enumerate(lines))

    return d




