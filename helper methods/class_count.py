import numpy as np
from collections import defaultdict

types = np.genfromtxt("Spectra Class.txt", unpack=True, usecols=[2], dtype='unicode')

counter = defaultdict(int)

for a in types:
    counter[a] += 1


print(counter)

#'F': 124500, 'M': 46519, 'A': 33113, 'K': 45743, 'B': 13458, 'G': 33465, 'O': 1970