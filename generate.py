import argparse
from random import randint
import training.file_management as file_management
from music21 import converter, instrument, note, chord, stream
from music_generator.voter import Voter
import utils

parser = argparse.ArgumentParser(description='Generate music')
parser.add_argument('voters', help='The path to the file containing the names of the voter networks')
parser.add_argument('-l', '--length', help='The number of notes generated', type=int, default=300)
parser.add_argument('-o', '--output', help='The name of the output', default='output')

args = parser.parse_args()

with open(args.voters, 'r') as f:
    voters = [Voter(v) for v in f.read().split('\n')]

note_mappings = file_management.load_note_mappings('note_mappings.csv')
num_notes = len(note_mappings)
previous_notes = [randint(0, num_notes - 1) for i in range(0, 100)]

for i in range(0, args.l):
    voted_notes = dict()
    for v in voters:
        vote = v.get_next_note_vote(previous_notes[-100:])
        if voted_notes[vote]:
            voted_notes[vote] = voted_notes[vote] + 1
        else:
            voted_notes[vote] = 1

    max = -1
    max_note = -1
    for n in voted_notes:
        if voted_notes[n] > max:
            max = voted_notes[n]
            max_note = n

    previous_notes.append(max_note)

generated_sequence = previous_notes[100:]
generated_notes = [note.Note('C4')]

for i in generated_sequence:
    note, offset = utils.category_to_note_and_offset(i)
    generated_notes.append(utils.get_note_from_interval_and_offset(generated_notes[-1], note, offset))

midi_stream = stream.Stream(generated_notes)

midi_stream.write('midi', fp=(args.o + '.mid'))
midi_stream.show()






