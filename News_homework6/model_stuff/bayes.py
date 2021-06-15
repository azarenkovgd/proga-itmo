import itertools
import math
import operator
import typing as tp
from collections import Counter, defaultdict
from copy import deepcopy


class NaiveBayesClassifier:
    def __init__(self, alpha):
        if not (0.0 < alpha <= 1.0):
            raise ValueError("Некорректное значение альфы")

        self.class_probs = []
        self.alpha = alpha
        self.dataset_size = 0
        self.unique_words = []
        self.words_per_class = []
        self.class_lengths = {}
        self.word_probs = []
        self.is_trained = False

    def fit(self, X: tp.List[str], y: tp.List[str]):
        assert len(X) == len(y)

        self.dataset_size = len(y)
        self.class_probs = Counter(y)  # Сколько раз определённая метка встречается в датасете
        class_names = sorted(list(set(y)))

        for class_name in self.class_probs:
            self.class_probs[class_name] /= len(y)

        unique_words = [el.split() for el in X]
        unique_words = list(itertools.chain.from_iterable(unique_words))
        unique_words = sorted(list(set(unique_words)))
        self.unique_words = unique_words

        self.words_per_class = defaultdict(dict)
        self.class_lengths = defaultdict(int)

        for i, string in enumerate(X):
            words = string.split()
            target = y[i]
            self.class_lengths[target] += len(words)

            for word in words:
                if word not in self.words_per_class:
                    self.words_per_class[word] = {class_name: 0 for class_name in class_names}
                self.words_per_class[word][target] += 1

        self.word_probs = deepcopy(self.words_per_class)
        for word, value in self.word_probs.items():
            for class_name, _ in value.items():
                self.word_probs[word][class_name] = (self.word_probs[word][class_name] + self.alpha) / (
                    self.class_lengths[class_name] + self.alpha * len(self.unique_words)
                )

        self.is_trained = True
        return

    def predict(self, X):
        assert self.is_trained

        labels = []

        for document in X:
            words = document.split()
            probabilities = defaultdict(float)

            for class_name in self.class_lengths.keys():
                word_probs_sum = []
                for word in words:
                    if word in self.unique_words:
                        word_probs_sum.append(math.log(self.word_probs[word][class_name]))
                word_probs_sum = sum(word_probs_sum)
                probabilities[class_name] = math.log(self.class_probs[class_name]) + word_probs_sum

            predicted_label = max(probabilities.items(), key=operator.itemgetter(1))[0]
            labels.append(predicted_label)
        return labels

    def score(self, X_test, y_test):
        predicted = self.predict(X_test)
        class_accuracies = defaultdict(float)

        for class_name in list(set(y_test)):
            if y_test.count(class_name):
                true_positives = sum(
                    [1 for i, e in enumerate(predicted) if e == class_name and y_test[i] == class_name]
                )
                false_negatives = sum(
                    [1 for i, e in enumerate(predicted) if e != class_name and y_test[i] == class_name]
                )
                class_accuracies[class_name] = true_positives / (true_positives + false_negatives)
        score = sum([i for i in class_accuracies.values()]) / len(list(set(y_test)))
        return score
