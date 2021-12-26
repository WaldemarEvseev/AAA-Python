from typing import Callable, Generator, Sequence, Union, TypeVar
from itertools import islice

T = TypeVar('T')


class Seq:
    def __init__(self, sequence: Union[Sequence[T], Generator]):
        self.seq = sequence

    @staticmethod
    def _map(sequence: Union[Sequence[T], Generator],
             func: Callable) -> Generator:
        """Создает генератор для метода map"""
        for t in sequence:
            yield func(t)

    def map(self, func: Callable):
        """
        Принимает функцию, которая будет трансформировать тип Т
        (тот который внутри последовательности, которую передали в инит)
        в любой тип.
        """
        return self.__class__(self._map(self.seq, func))

    @staticmethod
    def _filter(sequence: Union[Sequence[T], Generator],
                func: Callable) -> Generator:
        """Создает генератор для метода filter"""
        for t in sequence:
            if func(t):
                yield t

    def filter(self, func: Callable):
        """
        Принимает функцию, которая входным параметром принимает тип T
        и возвращает bool
        """
        return self.__class__(self._filter(self.seq, func))

    def take(self, num: int):
        """
        Принимает число и возвращает список
        из того количества элементов, которое передали в take
        """
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
