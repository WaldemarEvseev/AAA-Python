import json


class DynamicAttrs:
    def __init__(self, ad):
        if isinstance(ad, dict):
            self._ad = ad
        else:
            self._ad = json.loads(ad)

    def __getattr__(self, item):
        if not isinstance(self._ad[item], dict):
            return self._ad[item]
        return self.__class__(self._ad[item])


class BaseAdvert(DynamicAttrs):
    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


class ColorizeMixin:
    repr_color_code = 32  # green

    def __repr__(self):
        return f'\033[1;{self.repr_color_code};40m {super().__repr__()}\n'


class Advert(ColorizeMixin, BaseAdvert):
    def __init__(self, ad):
        super().__init__(ad)
        if 'price' not in self._ad:
            self.price = 0
        elif self._ad['price'] == -1:
            raise ValueError('must be >= 0')
        else:
            self.price = self._ad['price']


if __name__ == '__main__':
    # Test
    # создаем экземпляр класса Advert из JSON
    lesson_str = """{
    "title": "python", "price": 0, 
    "location": {"address": "город Москва, Лесная, 7", 
    "metro_stations": ["Белорусская"]}}"""
    lesson_ad = Advert(lesson_str)
    # обращаемся к атрибуту location.address
    assert lesson_ad.location.address == 'город Москва, Лесная, 7'

    # меняет цвет теĸста при выводе на ĸонсоль
    print(lesson_ad)

    # в случае отстувия поля price в JSON-объеĸте возвращает 0
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    assert lesson_ad.price == 0
