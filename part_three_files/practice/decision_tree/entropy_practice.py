import math
from collections import defaultdict, Counter

import numpy as np


def entropy(instances, class_index=0, attribute_name=None, value_name=None):
    num_instances = len(instances)
    if num_instances <= 1:
        return 0
    value_counts = defaultdict(int)
    for instance in instances:
        value_counts[instance[class_index]] += 1
    num_values = len(value_counts)
    if num_values <= 1:
        return 0
    attribute_entropy = 0.0
    for value in value_counts:
        value_probability = value_counts[value] / num_instances
        child_entropy = value_probability * math.log(value_probability, 2)
        attribute_entropy -= child_entropy
    return attribute_entropy


def uniquecounts(rows):
    results = {}
    for row in rows:
        # The result is the last column
        r = row[len(row) - 1]
        if r not in results: results[r] = 0
        results[r] += 1
    return results


# Entropy is the sum of p(x)log(p(x)) across all the different possible results
def entropy(rows):
    log2 = lambda x: math.log(x) / math.log(2)
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent


def entropy(s):
    res = 0
    val, counts = np.unique(s, return_counts=True)
    freqs = counts.astype('float') / len(s)
    for p in freqs:
        if p != 0.0:
            res -= p * np.log2(p)
    return res


def entropy(dataset):
    """Measure of the amount of uncertainty in the given dataset."""

    N = len(dataset)
    counter = Counter(dataset)
    return sum(-1.0 * (counter[k] / N) * math.log(counter[k] / N, 2) for k in counter)


def entropy(class_vector):
    """Compute the entropy for a list
    of classes (given as either 0 or 1)."""
    list = class_vector.tolist()
    if len(list) > 0:
        positive = float(list.count(1))
        negative = float(list.count(0))
        p = float(positive / (positive + negative))
        if p == 0 or p == 1:
            return 0
        else:
            logs = np.log2([p, 1 - p])
            result = -p * logs[0] - (1 - p) * logs[1]
            return result
    return 0


def information_gain(previous_classes, current_classes):
    """Compute the information gain between the
    previous and current classes (each
    a list of 0 and 1 values)."""
    remainder = 0
    num_examples = float(len(previous_classes))
    prev_entropy = entropy(previous_classes)

    for classification in current_classes:
        class_examples = float(len(classification))
        class_entropy = entropy(np.array(classification))
        remainder += (class_examples / num_examples) * class_entropy

    return prev_entropy - remainder


def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq / len(data)) * math.log(freq / len(data), 2)
    return data_entropy


# Entropy is the sum of p(x)log(p(x)) across all
# the different possible results
def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent
