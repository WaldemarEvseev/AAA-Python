import random
import abc


# Задание #1: Pokemon/обучение
# Дана функция обучения покемона train
# Измените класс Pokemon так, чтобы обучение проходило без ошибок

# Задание #2: Digimon/обучение
# Напишите класс Digimon так, чтобы обучение проходило без ошибок
# class Digimon:

# Задание #3: Digimon/ABC
# Напишите абстрактный класс AnimeMon:
# ● Имеет абстрактный метод inc_exp
# ● Имеет абстрактное свойство exp
# ● Классы Digimon и Pokemon наследуются от AnimeMon


class AnimeMon(abc.ABC):
    @property
    @abc.abstractmethod
    def exp(self) -> int:
        """Возвращает опыт"""
        pass

    @abc.abstractmethod
    def inc_exp(self, value: int):
        """Увеличивает опыт"""
        pass


class Digimon(AnimeMon):
    def __init__(self, name: str, exp: int = 0):
        self.name = name
        self._exp = exp

    @property
    def exp(self) -> int:
        """Возвращает опыт"""
        return self._exp

    def inc_exp(self, value: int):
        """Увеличивает опыт"""
        self._exp += value * 8


class Pokemon(AnimeMon):
    def __init__(self, name: str, poketype: str, exp: int = 0):
        self.name = name
        self.poketype = poketype
        self._exp = exp

    @property
    def exp(self) -> int:
        """Возвращает опыт"""
        return self._exp

    def to_str(self) -> str:
        """Возвращает имя и тип покемона"""
        return f'{self.name}/{self.poketype}'

    def inc_exp(self, step_size: int):
        """Увеличивает опыт"""
        self._exp += step_size


def train(animemon: AnimeMon):
    """
    Тренирует объект через серию спарингов со случайным исходом
    для увеличения опыта
    """
    step_size, level_size = 10, 100
    sparring_qty = (level_size - animemon.exp % level_size) // step_size
    for i in range(sparring_qty):
        win = random.choice([True, False])
        if win:
            animemon.inc_exp(step_size)


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    train(bulbasaur)
    print(bulbasaur.exp)

    agumon = Digimon(name='Agumon')
    train(agumon)
    print(agumon.exp)
