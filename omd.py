# Guido van Rossum <guido@python.org>
import requests


def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input().lower()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()



def step2_umbrella():
    setup = 'Ну так вот, пришла как-то раз в бар утка с зонтиком. Бармен видит это и говорит: '

    # запрос к балабоба
    punchline = requests.post('https://yandex.ru/lab/api/yalm/text3',
                              headers={'Content-Type': 'application/json'},
                              json={"query": setup, "intro": 0, "filter": 1}).json()
    
    return f'{setup} {punchline["text"]}'

def step2_no_umbrella():
    setup = 'Ну так вот, пришел как-то раз в бар зонтик без утки. Бармен видит это и говорит: '

    # запрос к балабоба
    punchline = requests.post('https://yandex.ru/lab/api/yalm/text3',
                              headers={'Content-Type': 'application/json'},
                              json={"query": setup, "intro": 0, "filter": 1}).json()

    return f'{setup} {punchline["text"]}'


if __name__ == '__main__':
    print(step1())

