import numpy as np


class Array:
    def __init__(self, arr_size, increment):
        self.increment = increment
        self.arr_size = arr_size
        self.data = np.array([[None]*self.arr_size] * self.increment)
        self.capacity = self.increment
        self.size = 0

    def update(self, row):
        for r in row:
            self.add(r)

    def add(self, x):
        if self.size == self.capacity:
            self.capacity += self.increment
            newdata = np.array([[None]*self.arr_size] * self.capacity)
            newdata[:self.size] = self.data
            self.data = newdata

        self.data[self.size] = x
        self.size += 1

    def finalize(self):
        return self.data[:self.size]
