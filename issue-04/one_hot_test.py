from one_hot_encoder import fit_transform
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_empty():
    """Тестирует обработку исключения для пустого ввода"""
    with pytest.raises(TypeError):
        fit_transform()


def test_equal():
    """Тестирует равенство фактического результата с ожидаемым"""
    subjects = ['Statistics', 'Python', 'SQL']
    exp = [('Statistics', [0, 0, 1]),
           ('Python', [0, 1, 0]),
           ('SQL', [1, 0, 0])]
    res = fit_transform(subjects)
    assert res == exp


def test_not_in():
    """Тестирует отсутствие дубликатов с разным бинарным представлением"""
    subjects = ['Statistics', 'Python', 'SQL', 'Python']
    false_ans = [1, 0, 0, 0]
    res = (pair[1] for pair in fit_transform(subjects))
    assert false_ans not in res


def test_number():
    """
    Тестирует результат ввода одного числового элемента разных типов
    через длину бинарного представления (код должен состоять из одного элемент)
    """
    number = ['1', 1, 1.000]
    exp_len = 1
    res_len = len(fit_transform(number)[0][1])
    assert bool(res_len == exp_len)

