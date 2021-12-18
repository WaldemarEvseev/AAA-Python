import math
from collections import defaultdict
import re


class CountVectorizer:
    """Convert a collection of text to a matrix of token counts"""

    def __init__(self,
                 lowercase=True,
                 token_pattern=r'[\w\d\-]+'):

        self.lowercase = lowercase
        self.token_pattern = token_pattern
        self.feature_names = []
        self.term_matrix = []

    def get_feature_names(self) -> list:
        """Return feature names for a document-term matrix"""
        return self.feature_names

    def fit_transform(self, corpus: list) -> list:
        """Return a document-term matrix"""
        if not isinstance(corpus, list):
            return self.term_matrix

        counter_list = [0] * len(corpus)
        token_counts = defaultdict(lambda: counter_list.copy())
        for i, sentence in enumerate(corpus):
            if isinstance(sentence, str):
                sentence = sentence.lower() if self.lowercase else sentence
            else:
                continue
            tokens = re.findall(self.token_pattern, sentence)
            for token in tokens:
                token_counts[token][i] += 1

        self.feature_names = list(token_counts.keys())
        self.term_matrix = [[token_counts[f][i] for f in self.feature_names]
                            for i, sentence in enumerate(corpus)]
        return self.term_matrix


def tf_transform(count_matrix: list) -> list:
    """Convert a matrix of token counts to a tf matrix"""
    return [[round(f / sum(sentence), 3) for f in sentence]
            for sentence in count_matrix]


def idf_transform(count_matrix: list) -> list:
    """Convert a matrix of token counts to a idf matrix"""
    idf_list = []
    n = len(count_matrix)
    for i, token in enumerate(count_matrix[0]):
        idf = 0
        for doc in count_matrix:
            if doc[i]:
                idf += 1
        idf_list.append(round(math.log((n + 1)/(idf + 1)) + 1, 1))

    return idf_list


class TfidfTransformer:
    """Convert a matrix of token counts to a tf-idf matrix"""

    def fit_transform(self, count_matrix: list) -> list:
        """Return a tf-idf matrix"""
        tf_list = tf_transform(count_matrix)
        idf_list = idf_transform(count_matrix)
        return [[round(tf * idf, 3) for tf, idf in zip(doc, idf_list)]
                for doc in tf_list]


class TfidfVectorizer(CountVectorizer):
    """Convert a collection of text to a tf-idf matrix"""

    def __init__(self):
        super().__init__()
        self._tfidf_transformer = TfidfTransformer()

    def fit_transform(self, corpus: list) -> list:
        """Return a tf-idf matrix"""
        count_matrix = super().fit_transform(corpus)
        return self._tfidf_transformer.fit_transform(count_matrix)


if __name__ == '__main__':
    # TEST
    corpus = ['Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    true_names = ['crock', 'pot', 'pasta', 'never',
                  'boil', 'again', 'pomodoro', 'fresh',
                  'ingredients', 'parmesan', 'to', 'taste']
    assert vectorizer.get_feature_names() == true_names

    true_tfidf_matrix = [[0.2, 0.2, 0.286, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
    assert tfidf_matrix == true_tfidf_matrix
