import Levenshtein
import numpy as np
import random
import string


# Algorithm -------------------------------------------------------------------


def edit_distance(s, t):
    """Edit distance of strings s and t. O(len(s) * len(t)). Prime example of a
    dynamic programming algorithm. To compute, we divide the problem into
    overlapping subproblems of the edit distance between prefixes of s and t,
    and compute a matrix of edit distances based on the cost of insertions,
    deletions, matches and mismatches.
    """
    prefix_matrix = np.zeros((len(s) + 1, len(t) + 1))
    prefix_matrix[:, 0] = list(range(len(s) + 1))
    prefix_matrix[0, :] = list(range(len(t) + 1))
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            insertion = prefix_matrix[i, j - 1] + 1
            deletion = prefix_matrix[i - 1, j] + 1
            match = prefix_matrix[i - 1, j - 1]
            if s[i - 1] != t[j - 1]:
                match += 1  # -- mismatch
            prefix_matrix[i, j] = min(insertion, deletion, match)
    return int(prefix_matrix[i, j])


# Ensure that the algorithm was correctly implemented --------------------------


def id_generator(size, chars=string.ascii_uppercase + string.digits):
    """Randomly generate an 'id' of characters and digits, taken from
    StackOverFlow question #2257441.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_string(min=1, max=20):
    """Generate a random 'id' string of a random length
    """
    size = random.randint(min, max)
    return id_generator(size)


# Generate random strings
random.seed(100)
random_strings1 = [generate_random_string() for _ in range(1000)]
random_strings2 = [generate_random_string() for _ in range(1000)]

# Compute edit distances using my function, and Levenshtein.distance
edit_distances_jake = [edit_distance(a, b) for a, b in
                       zip(random_strings1, random_strings2)]
edit_distances_lev = [Levenshtein.distance(a, b) for a, b in
                      zip(random_strings1, random_strings2)]

# Are the edit distances the same?
edit_distances_jake == edit_distances_lev
