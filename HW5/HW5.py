"""HW5 Чернышов Алексей"""

# ✔ 1. Создать view-функцию, которая возвращает количество уникальных имен (FirstName) в таблице Customers.
# ✔ 2. Создать view-функцию, которая выводит количество записей из таблицы Tracks.
# ✔ 3. Создать view-функцию, которая возвращает содержимое таблицы Customers с фильтрацией по всем текстовым полям
#   (оператор OR в sql-запросе). Параметры опциональные, если не переданы, то отбираются все записи.
# ✔ 4. Вывести сумму всех продажи компании из таблицы Invoice_Items как сумму всех произведений (UnitPrice * Quantity)
# ✔ 5. Вывести общую длительность треков в таблице в секундах, сгруппированную по музыкальным жанрам

from flask import Flask, render_template, abort, Response
from utils import execute_query, format_counter_to_int, format_counter_to_float, customers_params, EX_TEXT, MENU_BUTTONS
from webargs.flaskparser import use_kwargs
import queries
import status_codes


app = Flask(__name__)


@app.errorhandler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
@app.errorhandler(status_codes.HTTP_404_NOT_FOUND)
def error_404(err):
    return Response(render_template('error.html', code=err.code, menu=MENU_BUTTONS), status=err.code)


@app.route('/')
def index():
    return render_template('index.html', title='Main Page', data='Main Page', menu=MENU_BUTTONS, exercises=EX_TEXT)


@app.route('/unique_names')
def get_unique_names():
    query = queries.UniqueNameQuery
    res = format_counter_to_int(execute_query(query))
    return render_template('unique_names.html', title='Unique names', data=res, menu=MENU_BUTTONS)


@app.route('/tracks_count')
def get_tracks_count():
    query = queries.TracksCountQuery
    res = format_counter_to_int(execute_query(query))
    return render_template('tracks_count.html', title='Track counter', data=res, menu=MENU_BUTTONS)


@app.route('/customers')
@use_kwargs(customers_params, location='query')
def get_customers(text):
    fields = execute_query(queries.GetFieldsQuery)

    query = queries.CustomersNoParamQuery
    if text:
        query += queries.add_params_to_customers_query(text)

    data = execute_query(query)
    if not data:
        abort(422)

    return render_template('customers.html', title='Customers', fields=fields, data=data, text=text, menu=MENU_BUTTONS)


@app.route('/sales')
def get_sales():
    field_1_to_count = 'UnitPrice'
    field_2_to_count = 'Quantity'

    query = queries.add_params_to_sales_query(field_1_to_count, field_2_to_count)
    res = format_counter_to_float(execute_query(query))

    return render_template('sales.html', title='Sales', data=res, menu=MENU_BUTTONS)


@app.route('/genres')
def get_genres():
    fields = ('Genre', 'Duration')
    query = queries.GenresQuery
    data = execute_query(query)
    return render_template('genres.html', title='Genres', fields=fields, data=data, menu=MENU_BUTTONS)


if __name__ == '__main__':
    app.run(debug=True)
