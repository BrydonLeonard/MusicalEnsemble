import threading
import midi_data_extraction.midi_extract_utils as midi_extract_utils
import utils

files_per_batch = 20


class MidiDataExtractionThread(threading.Thread):
    def __init__(self, counter, midi_list, midi_list_lock):
        threading.Thread.__init__(self)
        self.counter = counter
        self.midi_list = midi_list
        self.midi_list_lock = midi_list_lock
        self.midi_list_len = len(self.midi_list)
        print('Initialised thread ' + str(self.counter))

    def run(self):
        print('Started thread ' + str(self.counter))
        while self.midi_list_len > 0:
            midi_sublist = []

            self.midi_list_lock.acquire()
            self.midi_list_len = len(self.midi_list)
            if self.midi_list_len > 0:
                midi_sublist = self.midi_list[:files_per_batch]
                del self.midi_list[:min(files_per_batch, self.midi_list_len)]
                self.midi_list_len = len(self.midi_list)
                print('  ' + str(self.midi_list_len) + ' files remaining')
            self.midi_list_lock.release()

            self.extract_data(midi_sublist)
        print('Finished thread ' + str(self.counter))


    def extract_data(self, midi_files):
        data_to_write = dict()

        print('  Thread ' + str(self.counter) + ' parsing...')
        for file in midi_files:
            print('    Thread ' + str(self.counter) + ' parsing ' + file)
            sequence = midi_extract_utils.extract_sequence_from_midi_file(file)
            data_from_sequence = midi_extract_utils.make_training_data_from_sequence(sequence)
            csv_file_name = file.replace('.mid', '.csv')
            data_to_write[csv_file_name] = data_from_sequence

        print('  Thread ' + str(self.counter) + ' writing data')
        for csv_file_name in data_to_write:
            with open(csv_file_name, 'w') as csv_file:
                for pattern in data_to_write[csv_file_name]:
                    notes = []
                    # The sequence of interval/duration pairs needs to be changed into indeces to become training data
                    for n in pattern:
                        notes.append(utils.note_to_category(n[0], n[1]))

                    csv_file.write(','.join([str(i) for i in notes]) + '\n')








