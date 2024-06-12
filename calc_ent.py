import math
from collections import Counter


def calculate_entropy(words):
    total_chars = sum(len(word) for word in words)
    char_counts = Counter(''.join(words))
    probabilities = {char: count / total_chars for char, count in char_counts.items()}

    entropy = -sum(prob * math.log2(prob) for prob in probabilities.values())
    return entropy
