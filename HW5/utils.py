import sqlite3
from webargs import fields

EX_TEXT = ('ex.1 Создать view-функцию, которая возвращает количество уникальных имен (FirstName) в таблице Customers.',
           'ex.2 Создать view-функцию, которая выводит количество записей из таблицы Tracks.',
           'ex.3 Создать view-функцию, которая возвращает содержимое таблицы Customers с фильтрацией по всем текстовым '
           'полям (оператор OR в sql-запросе). Параметры опциональные, если не переданы, то отбираются все записи.',
           'ex.4 Вывести сумму всех продажи компании из таблицы Invoice_Items как сумму всех произведений '
           '(UnitPrice * Quantity)',
           'ex.5 Вывести общую длительность треков в таблице в секундах, сгруппированную по музыкальным жанрам'
           )

MENU_BUTTONS = [  # Main menu buttons (headers)
    {'name': 'Main Page', 'url': '/'},
    {'name': 'Unique Names [ex.1]', 'url': '/unique_names'},
    {'name': 'Tracks count [ex.2]', 'url': '/tracks_count'},
    {'name': 'Customers [ex.3]', 'url': '/customers'},
    {'name': 'Sales [ex.4]', 'url': '/sales'},
    {'name': 'Genres [ex.5]', 'url': '/genres'},
]


customers_params = {
        "text": fields.Str(
            required=False,
            missing=None,
        )
    }


def execute_query(query, args=()):
    with sqlite3.connect('chinook.db') as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        records = cur.fetchall()
    return records


def format_counter_to_int(arg: list):
    return int(arg[0][0])


def format_counter_to_float(arg: list):
    return float(arg[0][0])
