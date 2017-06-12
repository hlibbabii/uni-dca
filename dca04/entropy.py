from collections import Counter
from math import log


def compute_entropy(char_list):
    counter = Counter(char_list)
    char_count = len(char_list)
    probabilities = (float(n)/char_count for n in counter.values())
    return sum(-p * log(p, 2) for p in probabilities)

with open('../resources/digits.txt', 'r') as f:
    print compute_entropy(f.read())
