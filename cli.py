import click
import abc
from random import randint
from typing import Callable, Dict, Tuple


# Описание рецептов классами
class Pizza(abc.ABC):
    def __init__(self, size: str = 'L'):
        # Словарь размеров блюд
        # и мультипликаторов для количества ингредиентов
        self.mult_dict = {'L': 1, 'XL': 2}

        if size.upper() in self.mult_dict.keys():
            self.size = size.upper()
        else:
            raise ValueError("Неверный размер пицц")

    @abc.abstractmethod
    def dict(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.size == other.size
        return False


def get_recipe(recipe: dict,
               size: str,
               mult_dict: Dict[str, int]) -> Dict[str, Tuple[int, str]]:

    """Выводит рецепт в зависимости от размера блюда"""
    x = mult_dict[size]
    return {ingredient: (x * params[0], params[1]) for ingredient, params
            in recipe.items()}


class Margherita(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍅'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'tomatoes': (1, '')}

    def dict(self):
        return get_recipe(self.recipe, self.size, self.mult_dict)


class Pepperoni(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍕'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'pepperoni': (200, 'g')}

    def dict(self):
        return get_recipe(self.recipe, self.size, self.mult_dict)


class Hawaiian(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍍'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'chicken ': (250, 'g'),
                       'pineapples': (1, '')}

    def dict(self):
        return get_recipe(self.recipe, self.size, self.mult_dict)


# Функции для вывода статуса заказа
def log(pattern) -> Callable:
    """Выводит имя функции и время выполнения"""
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            time = randint(1, 100)
            answer = pattern.format(time)
            print(answer)
        return wrapper
    return decorator


@log('bake — {}с!')
def bake(pizza: Pizza):
    """Готовит пиццу"""


@log('🛵 Доставили за {}с!')
def delivery(pizza: Pizza):
    """Доставляет пиццу"""


@log('🏠 Забрали за {}с!')
def pickup(pizza: Pizza):
    """Самовывоз"""


# Настройки пользовательского интерфейса
@click.group()
def cli():
    pass


@cli.command()
@click.option(' =delivery', 'with_delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: Pizza, with_delivery: bool):
    """Готовит и доставляет пиццу"""
    bake(pizza)
    if with_delivery:
        delivery(pizza)
    else:
        pickup(pizza)


@cli.command()
def menu():
    """Выводит меню"""
    for cl in (Margherita(), Pepperoni(), Hawaiian()):
        ingredients = ', '.join(cl.dict().keys())
        print(f'- {cl.__class__.__name__} {cl.icon}: {ingredients}')


if __name__ == '__main__':
    cli()
