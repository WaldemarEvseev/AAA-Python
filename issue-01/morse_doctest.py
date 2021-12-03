import os
import sys
import doctest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import morse


def doctest_encode(message: str) -> str:
    """
    Проверяет функцию encode из morse.py
    с помощью тестов, заданных в docstring
    >>> doctest_encode('SOS')
    '... --- ...'
    >>> doctest_encode('sos') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    KeyError: 's'
    >>> [doctest_encode(message)
    ... for message in ['SOS', 'AAA']] # doctest: +NORMALIZE_WHITESPACE
    ['... --- ...',
    '.- .- .-']
    """
    return morse.encode(message)


if __name__ == '__main__':
    doctest.testmod()
