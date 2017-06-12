import re
from collections import Counter

from math import log


def get_binary_weights(vectors):
    for vector in vectors:
        for key in vector:
            if vector[key] > 0:
                vector[key] = 1
    return vectors


def sum_vectors(vectors):
    sum = {k: 0 for k in set(vectors[0])}
    for binary_weight in vectors:
        sum = {k: sum.get(k) + binary_weight.get(k) for k in set(sum)}
    sum = {k: sum.get(k) for k in set(sum)}
    return sum


def get_tfidf_weights(vectors):
    sum = sum_vectors(vectors)
    for vector in vectors:
        for key in vector:
            vector[key] *= log(float(len(vectors)) / sum.get(key))
    return vectors



def get_centroid(binary_weights):
    sum = sum_vectors(binary_weights)
    centroid = {k: float(sum.get(k)) / len(binary_weights) for k in sum}
    return centroid


def classify(filename):
    classes = ['course', 'faculty', 'student', 'project']
    classes_map = {clazz: [] for clazz in classes}
    with open(filename, 'r') as f:
        documents = f.readlines()
        all_words = set()
        for document in documents:
            words = re.findall(r"[\w']+", document)
            first_word = words[0]
            occurences = Counter(words)
            all_words = all_words.union(occurences.keys())
            classes_map[first_word].append(dict(occurences))
    for document_clazz in classes_map.values():
        for document in document_clazz:
            zeros = {key: 0 for key in all_words if key not in document}
            document.update(zeros)
    return classes_map


filename = '../resources/webkb-train-stemmed1.txt'
document_classes_map = classify(filename)
# for document_class in document_classes_map.iteritems():
#     binary_weights = get_binary_weights(document_class[1])
#     print document_class[0]
#     print get_centroid(binary_weights)
all_documents = []
for documents in document_classes_map.values():
    all_documents.extend(documents)
tfidf_weights = get_tfidf_weights(all_documents)
print tfidf_weights




