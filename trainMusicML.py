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

modelName = 'placeholder'

print('Model name is "' + modelName + '"')

training_data = fileManagement.get_training_data('testMidiFolder')
noteMapping = fileManagement.load_note_mappings()
numUniqueNotes = len(noteMapping)

sequenceLength = 100 + 1

training_patterns = []

for i in range(sequenceLength, len(training_data)):
    seq = training_data[i-sequenceLength:i]
    training_patterns.append([noteMapping[j] for j in seq])

numPatterns = len(training_patterns)
noteSequences = array(training_patterns)

X, y = noteSequences[:, :-1], noteSequences[:, -1]
X = X.reshape(numPatterns, sequenceLength - 1, 1)
X = X / float(numUniqueNotes)
y = to_categorical(y, num_classes=numUniqueNotes)

model = Sequential()
model.add(LSTM(512, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dense(256, activation='softmax'))
model.add(Dropout(0.3))
model.add(Dense(numUniqueNotes, activation='softmax'))
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
