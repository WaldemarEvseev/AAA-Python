import morse
import os
import sys
import doctest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def doctest_encode(message: str) -> str:
    """
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
