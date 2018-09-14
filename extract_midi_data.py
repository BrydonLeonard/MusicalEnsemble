import glob
import os
import threading
from midi_data_extraction.midi_data_extract_thread import MidiDataExtractionThread
import argparse


parser = argparse.ArgumentParser(description='Extract training data from midi files')
parser.add_argument('-e', help='Extract midi files', action='store_true')
parser.add_argument('-g', help='Create genre-groupings', action='store_true')

args = parser.parser_args()

num_cores = 4

#Parses midi files into data stored in csvs in the same folder structure
def parse_midi_files_threaded(root_folder):
    print('Starting midi parse...')

    print('Finding files...')
    midi_file_list = []
    midi_file_list_lock = threading.Lock()
    for folder in glob.glob(root_folder + '/*'):
        if os.path.isdir(folder):
            for file in glob.glob(folder + '/*.mid'):
                midi_file_list.append(file)
    print(str(len(midi_file_list)) + ' files found')

    threads = []
    for i in range(0, num_cores):
        threads.append(MidiDataExtractionThread(i, midi_file_list, midi_file_list_lock))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print('Midi parse done.')


# Parses the csvs created by parse_midi_files_threaded and sorts them by genre
def parse_csv_files(root_folder):
    print('Starting csv parse')

    print('  Reading in genres')
    with open('genres.csv', 'r') as f:
        genres = dict((g, []) for g in f.read().split('\n'))
    print('  ' + str(len(genres)) + ' genres found')

    print('  Reading csvs...')
    for folder in glob.glob(root_folder + '/*'):
        if os.path.isdir(folder):
            print('    Checking folder ' + folder)
            for file in glob.glob(folder + '/*.mid'):
                with open(file, 'r') as f:
                    data = f.read().split('\n')

                    for g in genres:
                        if g in file:
                            genres[g].extend(data)

    print('  Writing genres')
    for g in genres:
        data = genres[g]
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/' + g + '.csv', 'w') as file:
            file.write('\n'.join(data))

    print('  Writing genre summary')
    with open('data/genres.csv', 'w') as file:
        for g in genres:
            num_patterns = len(genres[g])

            file.write(g + ',' + str(num_patterns) + '\n')

    print('csv parse done')


def run():
    if args.e:
        parse_midi_files_threaded('midi/genres')
    if args.g:
        parse_csv_files('midi/genres')

    print('Done')


run()
