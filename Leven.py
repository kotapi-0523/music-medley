import Levenshtein
import numpy as np


def distance(data):
    result_data = np.zeros((len(data), len(data)))

    for i in range(len(data)):
        for j in range(len(data)):
            result_data[i, j] = Levenshtein.distance(data[i], data[j])
    return result_data
