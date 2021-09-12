# Guido van Rossum <guido@python.org>
import requests


def step1(setup_1, setup_2):
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
        return step2(setup_1)
    return step2(setup_2)


def step2(setup):
    # запрос к балабоба
    punchline = requests.post('https://yandex.ru/lab/api/yalm/text3',
                              headers={'Content-Type': 'application/json'},
                              json={"query": setup, "intro": 0, "filter": 1}).json()
    
    return f'{setup} {punchline["text"]}'




if __name__ == '__main__':
    setup_umbrella = 'Ну так вот, пришла как-то раз в бар утка с зонтиком. Бармен видит это и говорит: '
    setup_no_umbrella = 'Ну так вот, пришел как-то раз в бар зонтик без утки. Бармен видит это и говорит: '
    print(step1(setup_umbrella, setup_no_umbrella))

