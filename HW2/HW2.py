"""HW2 Чернышов Алексей"""

#  1. Установить git. Результат: git version 2.24.1.windows.2                                                  ✔done

#  2. Зарегистрироваться на github.com или другом аналогичном сервисе.                                         ✔done
#  Результат: https://github.com/AlexFoxalt/HillelHomeworksPart2

#  3. Создать view-функцию, которая возвращает содержимое файла с установленными пакетами в текущем проекте    ✔done
#  (Pipfile.lock)
#  4. Создать view-функцию, которая возвращает список случайных студентов. Использовать библиотеку faker.      ✔done
#  5. [необязательно] Создать view-функцию, которая будет возвращать средний рост и средний вес                ✔done
#  (в см и кг соответственно) для студентов из файла hw.csv

from flask import Flask
from faker import Faker
from random import randint
import csv

fake = Faker('UK')
INCH_TO_CM = 2.54
POUNDS_TO_KG = 2.205

app = Flask(__name__)


@app.route("/")
def landing():
    """
    Landing of web site.

    :return: Some info about possible routes.
    """
    return "It's my site.<br>" \
           "Possible routes:<br>" \
           "/pipfile<br>" \
           "/students<br>" \
           "/avr_data"


@app.route("/pipfile")
def get_pipfile():
    """
    Reads the content of file.

    :return: File's content as string.
    """
    with open('../Pipfile.lock', 'r') as file:
        return file.read()


@app.route("/students")
def get_random_students():
    """
    Generate a random list of random students.

    :return: Numbered list of students.
    """
    students = []
    res = []

    for repeat in range(randint(5, 20)):  # Generate the whole list.
        students.append(fake.name())

    for num, student in enumerate(students):  # Every student get his index number.
        res.append(f'{str(num)}: {student}')

    return '<br>'.join(res)


@app.route("/avr_data")
def get_avr_data():
    """
    Parse data from Excel file. Calculate an average data. Transform data into required values.

    :return: Information about students as str.
    """
    with open('hw.csv') as file:
        reader = list(csv.DictReader(file))
        total_height = 0
        total_weight = 0

        for row in reader[1:-1]:  # Since first item is a names of columns and last one is an empty list.
            total_height += float(row[' "Height(Inches)"'])
            total_weight += float(row[' "Weight(Pounds)"'])

        number_of_students = len(reader) - 2  # Parse the total number of students as int.

        total_height = total_height * INCH_TO_CM / number_of_students  # inch > cm.
        total_weight = total_weight / POUNDS_TO_KG / number_of_students  # pounds > kg.

        res = f'Average height = {round(total_height, 2)} cm.<br>' \
              f'Average weight = {round(total_weight, 2)} kg.'

        return res


app.run()
