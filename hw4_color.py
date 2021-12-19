from abc import ABC, abstractmethod


class ComputerColor(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass


class Color(ComputerColor):
    END = '\033[0'
    START = '\033[1;38;2'
    MOD = 'm'

    def __init__(self, red: int, green: int, blue: int):
        self.r = max(min(red, 255), 0)
        self.g = max(min(green, 255), 0)
        self.b = max(min(blue, 255), 0)

    def __repr__(self):
        rgb = f'{self.r};{self.g};{self.b}'
        return f'{self.START};{rgb}{self.MOD}●{self.END}{self.MOD}'

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return (self.b == other.b
                and self.g == other.g
                and self.r == other.r)

    def __add__(self, other):
        if not isinstance(other, Color):
            return False
        return Color(self.r + other.r,
                     self.g + other.g,
                     self.b + other.b)

    def __hash__(self):
        return hash((self.r, self.g, self.b))

    def __mul__(self, c):
        cl = -256 * (1 - c)
        F = (259 * (cl + 255)) / (255 * (259 - cl))
        return Color(int(F * (self.r - 128) + 128),
                     int(F * (self.g - 128) + 128),
                     int(F * (self.b - 128) + 128))

    __rmul__ = __mul__

    __str__ = __repr__


def print_a(color: ComputerColor):
    """Печатает букву 'A' с заданным цветом"""
    bg_color = 0.2 * color
    a_matrix = [
        [bg_color] * 19,
        [bg_color] * 9 + [color] + [bg_color] * 9,
        [bg_color] * 8 + [color] * 3 + [bg_color] * 8,
        [bg_color] * 7 + [color] * 2 + [bg_color] + [color] * 2 + [bg_color] * 7,
        [bg_color] * 6 + [color] * 2 + [bg_color] * 3 + [color] * 2 + [bg_color] * 6,
        [bg_color] * 5 + [color] * 9 + [bg_color] * 5,
        [bg_color] * 4 + [color] * 2 + [bg_color] * 7 + [color] * 2 + [bg_color] * 4,
        [bg_color] * 3 + [color] * 2 + [bg_color] * 9 + [color] * 2 + [bg_color] * 3,
        [bg_color] * 19,
    ]
    for row in a_matrix:
        print(''.join(str(ptr) for ptr in row))


if __name__ == '__main__':
    g = Color(0, 255, 0)
    print_a(g)

    print('\nС понижением контрастности:')
    print_a(0.5 * g)
