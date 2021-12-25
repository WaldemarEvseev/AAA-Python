from typing import Callable
from itertools import islice


class Seq:
    def __init__(self, sequence):
        self.seq = sequence

    @staticmethod
    def _map(sequence, func):
        for t in sequence:
            yield func(t)

    def map(self, func: Callable):
        return self.__class__(self._map(self.seq, func))

    @staticmethod
    def _filter(sequence, func: Callable):
        for t in sequence:
            if func(t):
                yield t

    def filter(self, func: Callable):
        return self.__class__(self._filter(self.seq, func))

    def take(self, num: int):
        return list(islice(self.seq, num))


if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]
    seq = Seq(numbers)
    res = seq.filter(lambda n: n % 2 == 0).map(lambda n: n + 10).take(3)
    print(res)
    assert res == [12, 14]

    numbers = [1, 2, 3, 4, 5, 6, 8, 10, 12]
    seq = Seq(numbers)
    res = seq.filter(lambda n: n % 2 == 0).map(lambda n: n + 10).take(3)
    print(res)
    assert res == [12, 14, 16]
