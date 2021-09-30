import csv
import math
from collections import defaultdict

# Названия команд
HIERARCHY_COMMAND = '1'
REPORT_COMMAND = '2'
SAVE_COMMAND = '3'
EXIT_COMMAND = '4'


# Предварительная обработка данных
def preprocess_csv(file_name='Corp_Summary.csv', encoding_type='utf-8') -> (list, list):
    """
    Возвращает исходные данные с правильной кодировкой
    headers = заголовок таблицы
    data = значения таблицы
    """
    data = []
    with open(file_name, 'r', encoding=encoding_type) as f:
        f = f.read().split('\n')
        headers = f[0].split(';')
        for line in f[1:]:
            if line != '':
                data.append(line.split(';'))
    return headers, data


# ЗАДАНИЕ №1
def get_hierarchy(data: list, dep_col_index: int, team_col_index: int) -> dict:
    """
    Возвращает иерахию в формате словаря
    ключ = департамент
    значение = множество отделов для одного департамента
    """
    hierarchy = {}
    for item in data:
        dep = item[dep_col_index].lower()
        team = item[team_col_index]
        if dep not in hierarchy:
            hierarchy[dep] = {team}
            continue
        if team not in hierarchy[dep]:
            hierarchy[dep].add(team)
    return hierarchy


def print_hierarchy(hierarchy: dict):
    """Выводит в консоль иерархию для выбранного департамента"""
    dep = ''
    print(f'Список департаментов: {", ".join(hierarchy.keys())}')
    while dep not in hierarchy:
        dep = input('Введите название департамента: ').lower()

    print(f'В департамент "{dep.capitalize()}" входит:')
    for team in hierarchy[dep]:
        print(f'- Отдел "{team}"')


# ЗАДАНИЕ №2
def get_stat(data: list, dep_col_index: int, salary_col_index: int) -> dict:
    """
    Считает статистику для департаментов по выбранным в scheme показателям
    """

    scheme = {'Численность': 0,
              'Мин. зарплата': math.inf,
              'Макс. зарплата': 0,
              'Средняя зарплата': 0,
              'ФОТ': 0}

    stat = defaultdict(lambda: scheme.copy())

    for item in data:
        dep = item[dep_col_index]
        salary = int(item[salary_col_index])

        stat[dep]['Численность'] += 1
        stat[dep]['ФОТ'] += salary
        if stat[dep]['Мин. зарплата'] > salary:
            stat[dep]['Мин. зарплата'] = salary
        if stat[dep]['Макс. зарплата'] < salary:
            stat[dep]['Макс. зарплата'] = salary

    for dep in stat.keys():
        total_salary = stat[dep]['ФОТ']
        staff = stat[dep]['Численность']
        stat[dep]['Средняя зарплата'] = round(total_salary / staff, 2)

    return stat


def prepare_stat_table(stat: dict) -> (list, list):
    """
    Подготавливает статистику (table) по департаментам для вывода в консоль,
    width_setting нужен для определения минимально допустимой длины столбца
    """

    table = []
    width_setting = []

    headers = []
    header = '| Название департамента'
    width_setting.append(len(header))
    headers.append(header)
    for key in stat[0].keys():
        header = f'| {key}'
        width_setting.append(len(header))
        headers.append(header)
    table.append(headers)

    for dep in stat:
        col_num = 0
        if dep == 0:
            continue
        values = []
        value = f'| {dep}'
        width_setting[col_num] = max(len(value), width_setting[col_num])
        values.append(value)
        for value in stat[dep].values():
            col_num += 1
            value = f'| {value}'
            width_setting[col_num] = max(len(value), width_setting[col_num])
            values.append(value)
        table.append(values)

    return table, width_setting


def print_table(table: list, width_setting: list, col_width=23):
    """
    Выводит в консоль таблицу со статистикой по департаментам
    и с учетом заданной длины столбцов (но не меньше минимально допустимой)
    """
    for dep_stat in table:
        row = ''
        for i, value in enumerate(dep_stat):
            value = str(value)
            space = max(width_setting[i] - len(value), col_width - len(value))
            row = f'{row}{value}{" "*space}'
        print(row)


# ЗАДАНИЕ №3
def write_csv(stat: dict, file_name: str):
    """Записывает статистику по департаментам в формате csv"""
    headers = []
    headers.append('Название департамента')
    for key in stat[0].keys():
        headers.append(key)

    with open(file_name, 'w') as f:
        out_file = csv.writer(f, delimiter=';')
        out_file.writerow(headers)
        for dep, stats in stat.items():
            if dep == 0:
                continue
            row = []
            row.append(dep)
            for value in stats.values():
                row.append(value)
            out_file.writerow(row)


if __name__ == '__main__':
    # Обработка данных
    headers, data = preprocess_csv()
    dep_col_index = headers.index('Департамент')
    team_col_index = headers.index('Отдел')
    salary_col_index = headers.index('Оклад')

    # Описание команд
    commands = {
        HIERARCHY_COMMAND: 'Иерархия: выводит иерархию команд '
                           'внутри выбранного департамента',
        REPORT_COMMAND: 'Отчет: выводит  название, численность '
                        'и интервал зарплат по каждому департаменту',
        SAVE_COMMAND: 'Cохранить: сохраняет сводный отчет',
        EXIT_COMMAND: 'Выйти: выходит из программы'
    }

    # Вывод и работа в консоли
    print('СПИСОК КОМАНД:')
    commands = {n: d for n, d in sorted(commands.items(), key=lambda x: x[0])}
    for num, description in commands.items():
        print(f'{num}. {description}')

    command = ''
    while command not in commands:
        command = input('\nВведите номер команды: ')
        if command == EXIT_COMMAND:
            break
        elif command == HIERARCHY_COMMAND:
            hierarchy = get_hierarchy(data, dep_col_index, team_col_index)
            print_hierarchy(hierarchy)
        elif command == REPORT_COMMAND:
            stat = get_stat(data, dep_col_index, salary_col_index)
            table, width_setting = prepare_stat_table(stat)
            print_table(table, width_setting)
        elif command == SAVE_COMMAND:
            stat = get_stat(data, dep_col_index, salary_col_index)
            write_csv(stat, './Stat.csv')
            print('Запись выполнена')
