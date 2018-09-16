from numpy import array
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from training import file_management
import utils
import argparse
import os

parser = argparse.ArgumentParser(description='Train on a midi dataset')
parser.add_argument('training_data', help='The path to the folder containing the training data')
parser.add_argument('genre', help='The genre to train')

args = parser.parse_args()

print('Model name is "' + args.genre + '"')

if not os.path.exists('models/'):
    os.mkdir('models')

X, y = file_management.load_training_data(args.training_data, args.genre)
note_mappings = file_management.load_note_mappings('note_mappings.csv')
numOutputs = len(note_mappings)

sequenceLength = 100 + 1

training_patterns = []

y = to_categorical(y, numOutputs)

model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(100, 1)))
model.add(Dropout(0.3))
model.add(LSTM(128))
model.add(Dropout(0.3))
model.add(Dense(128, activation='softmax'))
model.add(Dropout(0.3))
model.add(Dense(numOutputs, activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

file_path = 'models/' + args.genre + 'weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5'
checkpoint = ModelCheckpoint(
    file_path, monitor='loss',
    verbose=0,
    save_best_only=True,
    mode='min'
)    
callbacks_list = [checkpoint]     
model.fit(X, y, epochs=200, batch_size=64, callbacks=callbacks_list)

model.save('models/model_ ' + args.genre + '.h5')
