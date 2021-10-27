from collections import defaultdict
import re


class CountVectorizer():
    """Convert a collection of text to a matrix of token counts"""

    def __init__(self,
                 lowercase=True,
                 token_pattern=r"[\w\d\-]+"):

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
            raise Exception("Corpus isn't a list")

        token_counts = defaultdict(lambda: [0 for seq in corpus])
        if self.lowercase:
            for i, seq in enumerate(corpus):
                tokens = re.findall(self.token_pattern, str(seq).lower())
                for token in tokens:
                    token_counts[token][i] += 1
        else:
            for i, seq in enumerate(corpus):
                tokens = re.findall(self.token_pattern, str(seq))
                for token in tokens:
                    token_counts[token][i] += 1

        self.feature_names = [token for token in token_counts.keys()]
        self.term_matrix = [[token_counts[f][i] for f in self.feature_names]
                            for i, seq in enumerate(corpus)]
        return self.term_matrix


if __name__ == "__main__":
    # TEST
    # Test from the task
    corpus = ['Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    true_feature_name = ['crock', 'pot', 'pasta', 'never', 'boil', 'again',
                         'pomodoro', 'fresh', 'ingredients', 'parmesan',
                         'to', 'taste']
    true_term_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]

    assert vectorizer.get_feature_names() == true_feature_name
    assert count_matrix == true_term_matrix

    # Corpus isn't a list
    print('Test for inappropriate types of corpus')
    test_sample = ["I'm not a list", 123, ("I'm not a list", "Hello, corpus")]
    for false_corpus in test_sample:
        vectorizer = CountVectorizer()
        try:
            vectorizer.fit_transform(false_corpus)
        except Exception as e:
            print(e)

    # Empty corpus
    print('\nTest for an empty corpus')
    corpus = []
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(count_matrix)

    # Test for lowercase
    print('\nTest for lowercase=False')
    corpus = ['Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    vectorizer = CountVectorizer(lowercase=False)
    count_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(count_matrix)