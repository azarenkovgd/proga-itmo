import typing as tp

import nltk


def load_nltk_stuff():
    try:
        nltk.data.find("punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    try:
        nltk.data.find("stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)


def clear_sentence(sentence: str) -> str:
    stemmer = nltk.stem.SnowballStemmer("english")
    tokens: tp.List[str] = [
        stemmer.stem(token).lower()
        for token in nltk.word_tokenize(sentence)
        if token.isalnum() and token not in nltk.corpus.stopwords.words("english")
    ]

    return " ".join(tokens)


def clear_dataset(dataset: tp.List[str]):
    load_nltk_stuff()

    for i, sentence in enumerate(dataset):
        dataset[i] = clear_sentence(sentence)

    return dataset
