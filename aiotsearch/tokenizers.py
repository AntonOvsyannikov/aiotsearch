import threading

import pymorphy2

morph = pymorphy2.MorphAnalyzer()
morph.lock = threading.Lock()


def tokenize_naive(phrase) -> set:
    return set(map(lambda s: s.lower(), phrase.split(' ')))


def tokenize_pymorphy(phrase) -> set:
    words = tokenize_naive(phrase)
    res = set()
    with morph.lock:
        for word in words:
            p = morph.parse(word)[0]
            res.add(p.normal_form)
    return res
