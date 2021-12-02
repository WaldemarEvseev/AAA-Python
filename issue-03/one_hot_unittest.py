from one_hot_encoder import fit_transform
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestOneHotEncoder(unittest.TestCase):
    """
    Проверяет функцию fit_transform из one_hot_encoder.py
    с помощью тестов, заданных через фреймворк unittest
    """
    def test_empty(self):
        """Тестирует обработку исключения для пустого ввода"""
        with self.assertRaises(TypeError):
            fit_transform()

    def test_equal(self):
        """Тестирует равенство фактического результата с ожидаемым"""
        subjects = ['Statistics', 'Python', 'SQL']
        exp = [('Statistics', [0, 0, 1]),
               ('Python', [0, 1, 0]),
               ('SQL', [1, 0, 0])]
        res = fit_transform(subjects)
        self.assertEqual(res, exp)

    def test_not_in(self):
        """Тестирует отсутствие дубликатов с разным бинарным представлением"""
        subjects = ['Statistics', 'Python', 'SQL', 'Python']
        false_ans = [1, 0, 0, 0]
        res = (pair[1] for pair in fit_transform(subjects))
        self.assertNotIn(false_ans, res)

    def test_number(self):
        """
        Тестирует результат ввода одного числового элемента разных типов
        через длину бинарного представления (код должен состоять из одного элемент)
        """
        number = ['1', 1, 1.000]
        exp_len = 1
        res_len = len(fit_transform(number)[0][1])
        self.assertTrue(res_len == exp_len)


if __name__ == '__main__':
    unittest.main()

