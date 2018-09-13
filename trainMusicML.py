from numpy import array
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Dropout
from keras.layers import Activation
from keras.callbacks import ModelCheckpoint
import numpy as np
import fileManagement
import utils
import argparse

parser = argparse.ArgumentParser(description='Train on a midi dataset')
parser.add_argument('folder', help='The path to the folder containing the training data')
parser.add_argument('model_name', help='The name of the model')
parser.add_argument('--r', help='Reload the training data from the midi files', action="store_true")

args = parser.parse_args()

modelName = args.model_name

print('Model name is "' + modelName + '"')

X, y = fileManagement.load_training_data(args.folder, args.r)
note_mappings = fileManagement.load_note_mappings('midi/noteMappings.csv')
numOutputs = len(note_mappings)

sequenceLength = 100 + 1

training_patterns = []

y = array([utils.note_to_category(note[0], note[1]) for note in y])
y = to_categorical(y, numOutputs)

model = Sequential()
model.add(LSTM(512, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dense(256, activation='softmax'))
model.add(Dropout(0.3))
model.add(Dense(numOutputs, activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

file_path = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
checkpoint = ModelCheckpoint(
    file_path, monitor='loss',
    verbose=0,
    save_best_only=True,
    mode='min'
)    
callbacks_list = [checkpoint]     
model.fit(X, y, epochs=200, batch_size=64, callbacks=callbacks_list)

model.save('model_ ' + modelName + '.h5')
