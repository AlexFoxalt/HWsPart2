"""HW3 Чернышов Алексей"""

#  1. Выводит строку из length случайных символов англ алфавита.
#
# Принимает следующие необязательные аргументы:
#
# length. Регулирует длину случайной строки, значение по умолчанию: 10 specials. Регулирет включение спец символов
# англ алфавита в сгенерированную строку: !"№;%:?*$()_+. Работает как булевый параметр: 1 -> True, 0 -> False. По
# умолчанию символы не включаются. digits. Регулирет включение цифр в сгенерированную строку: 0123456789. Работает
# как булевый параметр: 1 -> True, 0 -> False. По умолчанию цифры не включаются. Предусмотреть проверку всех
# аргументов:
#
# length: число, в диапазоне от 1 до 100.
# specials: 0 или 1
# digits: 0 или 1
# get_password() -> 127.0.0.1:5000/password?length=42
#
#
# 2. Создать view-функцию, которая выводит курс биткойна для заданной валюты (https://bitpay.com/api/rates ). Для
# этого установить и использовать пакет requests: https://pypi.org/project/requests/. Параметр currency
# необязательный, по умолчанию используется USD.
#
# def get_bitcoin_rate() -> /bitcoin_rate?currency=UAH
#
#
# 3*. [Необязательно] Вернуть результаты заданий 1 и 2 в виде html-страницы (пример в аттаче). Для этого разобраться
# с тем, что такое шаблоны и как они рендерятся: https://pythonru.com/uroki/6-shablony-vo-flask

import string
from flask import Flask, request, render_template
import random
from requests import get

UPPER_LETTERS = string.ascii_uppercase
LOWER_LETTERS = string.ascii_lowercase
DIGITS = string.digits
SPECIALS = string.punctuation


def string_generator(arg: dict):
    """
    Generates a string according to the passed arguments.

    :param arg: Expected a dict of parsed params from url.
    :return: List of possible elements.
    """
    possible_elements = [*UPPER_LETTERS, *LOWER_LETTERS]

    if 'digits' in arg and arg['digits'] == '1':
        possible_elements.extend(DIGITS)

    if 'specials' in arg and arg['specials'] == '1':
        possible_elements.extend(SPECIALS)

    return possible_elements


app = Flask(__name__)


@app.route("/")
def landing():
    """
    Landing of web site.

    :return: Some info about possible routes.
    """
    return render_template('base.html', title='Main Page', name='My site')


@app.route("/password")
def get_password():
    """
    Parse all params that were passed to URL, sorting params with valuable names, and generate a new password.

    :return: Random password as .html file.
    """
    params = {}
    for param, value in request.args.items():
        params.update({param: value})

    try:
        length = int(params['length'])
        if length not in range(1, 101):
            raise Exception('Invalid value of "length" parameter.')
    except Exception as e:
        print(f'Error occurred: {e}')
        length = 10

    possible_symbols = string_generator(params)

    res = ''.join(random.choices(possible_symbols, k=length))

    return render_template('base.html',
                           title="Password Generator",
                           name='Password Generator',
                           data=res)


@app.route("/bitcoin_rate")
def get_bitcoin_rate():
    """
    Fetch the BTC rate from website. If param 'code' was passed, generates a value in such format.

    :return: BTC rate as .html file.
    """
    code = request.args.get('code', 'USD')

    url = 'https://bitpay.com/api/rates'

    try:
        response = get(url).json()
    except Exception as e:
        print(f'Error occurred:  {e}')
        return render_template('error.html', error_code='The request was unsuccessful.')

    for item in response:
        if item['code'] == code:
            return render_template('base.html',
                                   title='BTC actual rate',
                                   name='BTC rates',
                                   data=f'From BTC to {item["code"]} >>> {item["rate"]}')

    return render_template('error.html', error_code='No matches found! Try again with another code.')


@app.route("/codes")
def get_codes():
    """
    Collect all possible codes for actual datetime from website.

    :return: List of codes as .html file.
    """
    url = 'https://bitpay.com/api/rates'

    try:
        response = get(url).json()
        print(response)
    except Exception as e:
        print(f'Error occurred: {e}')
        return render_template('error.html', error_code='Connection with server was lost.')

    return render_template('codes.html', iter=response)


if __name__ == "__main__":
    app.run(debug=True)
