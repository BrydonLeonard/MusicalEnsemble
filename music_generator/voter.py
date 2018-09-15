from keras.models import load_model
import numpy as np
from numpy import array


class Voter:
    def __init__(self, model_file):
        self.model_file = model_file
        self.model = load_model(model_file)

    def get_next_note_vote(self, previous_notes):
        previous_notes_array = array(previous_notes)
        previous_notes_array.reshape((1, len(previous_notes), 1))

        predicted_note = self.model.predict(previous_notes_array, verbose=0)

        chosen_note = np.argmax(predicted_note)

        return chosen_note
