import numpy as np

from . import features
from .image import Image


class Matcher:
    def __init__(self, filenames):
        self.images = [Image(filename) for filename in filenames]
        self.features = [
            (features.vector, 0.42),
            (features.vertices_count, 0.33),
            (features.similarity, 0.25)
        ]
        self.n = len(filenames)
        self.matching = np.zeros((self.n, self.n))

    def match(self):
        weight_sum = sum(weight for _, weight in self.features)
        for i, j in self.each_pair():
            for feature, weight in self.features:
                score = feature(self.images[i], self.images[j]) * (weight / weight_sum)
                self.matching[i, j] += score
                self.matching[j, i] += score

    def best_matches(self):
        for i in range(self.n):
            row = self.matching[i, :]
            yield [j for j in np.argsort(-row) if j != i]

    def each_pair(self):
        for i in range(self.n):
            for j in range(self.n):
                if i < j:
                    yield (i, j)
