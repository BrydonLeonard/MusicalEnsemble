import glob
from numpy import array
import util_scripts.space_efficient_array as efficient


# def load_note_mappings():
#     note_mapping_file = open('notes.csv', 'r')
#
#     d = dict()
#
#     for line in note_mapping_file.read().split('\n'):
#         spl = line.split(',')
#         if len(spl) > 1:
#             d[spl[1]] = int(spl[0])
#
#     return d


def load_training_data(folder, genre):
    file_name = glob.glob(folder + '/*' + genre + '*.csv')[0]
    with open(file_name, 'r') as f:
        data = []
        output = []
        print('Loading data...')
        for line in f:
            line = line.rstrip()
            if line:
                spl = line.split(',')
                data.append([int(x) for x in spl[:-1]])
                output.append([int(spl[-1])])

    data = array(data)
    output = array(output)
    print(data[:3])
    print(output[:3])

    return data.reshape(len(data), 100, 1), output


def load_note_mappings(file_name):
    with open(file_name, 'r') as f:
        lines = [line for line in f.read().split('\n') if line]
    d = dict((key, value) for (value, key) in enumerate(lines))

    return d




