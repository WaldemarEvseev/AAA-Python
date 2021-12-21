import click
import abc
from random import randint
from typing import Callable, Dict, Tuple


# Описание рецептов классами
class Pizza(abc.ABC):
    def __init__(self, size: str = 'L'):
        if size in ('L', 'XL'):
            self.size = size
        else:
            raise ValueError("Неверный размер пицц")

    @abc.abstractmethod
    def dict(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.size == other.size
        return False


def get_recipe(recipe: dict, size: str, x: int) -> Dict[str, Tuple[int, str]]:
    """Выводит рецепт в зависимости от размера блюда"""
    if size == 'L':
        return recipe
    elif size == 'XL':
        return {ingredient: (x * param[0], param[1]) for ingredient, param
                in recipe.items()}


class Margherita(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍅'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'tomatoes': (1, '')}

    def dict(self):
        return get_recipe(self.recipe, self.size, 2)


class Pepperoni(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍕'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'pepperoni': (200, 'g')}

    def dict(self):
        return get_recipe(self.recipe, self.size, 3)


class Hawaiian(Pizza):
    def __init__(self, size: str = 'L'):
        super().__init__(size)
        self.icon = '🍍'
        self.recipe = {'tomato sauce': (115, 'g'),
                       'mozzarella ': (125, 'g'),
                       'chicken ': (250, 'g'),
                       'pineapples': (1, '')}

    def dict(self):
        return get_recipe(self.recipe, self.size, 2)


# Функции для вывода статуса заказа
def log(pattern: str) -> Callable:
    """Выводит имя функции и время выполнения"""
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            time = randint(1, 100)
            if pattern:
                answer = pattern.format(time)
            else:
                func_name = function(*args, **kwargs).__name__
                answer = f'{func_name} - {time}с!'
            print(answer)
        return wrapper
    return decorator


@log
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
@click.option(' =delivery', default=False, is_flag=True)
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
        print(f'- {cl.__name__} {cl.icon}: {ingredients}')


if __name__ == '__main__':
    cli()
    delivery(Margherita())
    bake(Margherita())
