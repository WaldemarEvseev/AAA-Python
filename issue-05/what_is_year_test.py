from what_is_year_now import what_is_year_now
import urllib.request
import os
import sys
from unittest.mock import patch
import pytest
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize('resp_json, exp', [
    ({'currentDateTime': '2021-12-31'}, 2021),
    ({'currentDateTime': '31.12.2021'}, 2021)
])
def test_what_is_year(resp_json: dict, exp: int):
    """
    Проверяет функцию what_is_year_now
    с помощью тестов, заданных через декоратор
    """
    with patch.object(urllib.request, 'urlopen'):
        with patch.object(json, 'load', return_value=resp_json):
            res = what_is_year_now()
    assert res == exp


def test_exception():
    """Тестирует обработку исключения для неправильного формата ввода"""
    with pytest.raises(ValueError):
        resp_json = {'currentDateTime': 'test for else'}
        with patch.object(urllib.request, 'urlopen'):
            with patch.object(json, 'load', return_value=resp_json):
                what_is_year_now()
