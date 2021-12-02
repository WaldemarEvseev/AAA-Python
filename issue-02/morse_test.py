import morse
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize('morse_message, exp', [
    ('... --- ...', 'SOS'),
    ('... --- ...', 'sos'),
    ('...---...', 'SOS')
])
def test_decode(morse_message: str, exp: str):
    """
    Проверяет функцию decode из morse.py
    с помощью тестов, заданных через декоратор
    """
    assert morse.decode(morse_message) == exp
