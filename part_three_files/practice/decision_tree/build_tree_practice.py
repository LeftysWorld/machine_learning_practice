def get_split_indices(x_train, num_instances):
    feature_index = randint(0, x_train.shape[1] - 1)
    split_index1, split_index2 = randint(0, num_instances - 1), randint(0, num_instances - 1)
    split_val = (x_train[split_index1][feature_index] + x_train[split_index2][feature_index]) / 2
    left_indices = [i for i in xrange(x_train.shape[0]) if x_train[i][feature_index] <= split_val]
    right_indices = [i for i in xrange(x_train.shape[0]) if x_train[i][feature_index] > split_val]
    return left_indices, right_indices, feature_index, split_val


def recursive_split(x, y):
    def is_pure(s):
        return len(set(s)) == 1

    # If there could be no split, just return the original set
    if is_pure(y) or len(y) == 0:
        return y
    # We get attribute that gives the highest mutual information
    gain = np.array([mutual_information(y, x_attr) for x_attr in x.T])
    selected_attr = np.argmax(gain)
    # If there's no gain at all, nothing has to be done, just return the original set
    if np.all(gain < 1e-6):
        return y
    # We split using the selected attribute
    sets = partition(x[:, selected_attr])
    res = {}
    for k, v in sets.items():
        y_subset = y.take(v, axis=0)
        x_subset = x.take(v, axis=0)
        res["x_%d = %d" % (selected_attr, k)] = recursive_split(x_subset, y_subset)
    return res


# Divides a set on a specific column. Can handle numeric or nominal values
def divideset(rows, column, value):
    # Make a function that tells us if a row is in the first group (true) or the second group (false)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):  # check if the value is a number i.e int or float
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    # Divide the rows into two sets and return them
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def loss(pairs):
    """
    L^2 loss - sum of squared divergence of label from average
    """
    if not pairs:
        return 0.0
    average_label = sum(l for _, l in pairs) / len(pairs)
    return sum((l - average_label) ** 2 for _, l in pairs)


def get_best_split(examples, features):
    best_feature, best_value, best_loss_reduction = \
        0, 0.0, 0.0
    for feature in features:
        pairs = sorted(
            [(e.features[feature], e.label) for e in examples])
        for index, (value, label) in enumerate(pairs):
            left, right = pairs[:index], pairs[index:]
            current_loss_reduction = \
                loss(left) + loss(right) - loss(pairs)
            if current_loss_reduction < best_loss_reduction:
                best_feature = feature
                best_value = value
                best_loss_reduction = current_loss_reduction

    return (best_feature, best_value, best_loss_reduction)


def recursive_split(x, y):
    def mutual_information(y, x):
        def entropy(s):
            res = 0
            val, counts = np.unique(s, return_counts=True)
            freqs = counts.astype('float') / len(s)
            for p in freqs:
                if p != 0.0:
                    res -= p * np.log2(p)
            return res

        res = entropy(y)
        # We partition x, according to attribute values x_i
        val, counts = np.unique(x, return_counts=True)
        freqs = counts.astype('float') / len(x)
        # We calculate a weighted average of the entropy
        for p, v in zip(freqs, val):
            res -= p * entropy(y[x == v])
        return res

    def is_pure(s):
        return len(set(s)) == 1

    # If there could be no split, just return the original set
    if is_pure(y) or len(y) == 0:
        return y

    # We get attribute that gives the highest mutual information
    gain = np.array([mutual_information(y, x_attr) for x_attr in x.T])
    selected_attr = np.argmax(gain)

    # If there's no gain at all, nothing has to be done, just return the original set
    if np.all(gain < 1e-6):
        return y

    # We split using the selected attribute
    sets = partition(x[:, selected_attr])

    res = {}
    for k, v in sets.items():
        y_subset = y.take(v, axis=0)
        x_subset = x.take(v, axis=0)

        res["x_%d = %d" % (selected_attr, k)] = recursive_split(x_subset, y_subset)

    return res


def split(self, data, start, end, candidates):
    colSplit = np.random.choice(candidates)
    elements = np.random.choice(range(start, end + 1), 2, replace=False)
    mean = (data[elements[0], colSplit] + data[elements[1], colSplit]) / 2
    newCol = np.empty([len(data), 1])
    for i in range(start, (end + 1)):
        if data[i, colSplit] >= mean:
            newCol[i] = 1
        else:
            newCol[i] = 0
    data = np.column_stack((data, newCol))
    data = data.tolist()
    data = sorted(data, key=lambda x: x[len(data[0]) - 1], reverse=True)
    data = np.array(data)
    splitInd = np.sum(data[:, (len(data[0]) - 1)])
    data = data[:, 0:(len(data[0]) - 1)]
    split1 = data[0:splitInd, :]
    split2 = data[splitInd:len(data), :]
    splitInfo = [colSplit, mean]
    return split1, split2, splitInfo
