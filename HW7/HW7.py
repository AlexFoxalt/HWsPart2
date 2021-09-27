"""HW7 Чернышов Алексей"""

# ✔ 1.Создать класс Point, отнаследованный от класса Shape. В классе Point будут только координаты точки. Реализовать
#   задание 6.5 с использованием базового класса Shape.
# ✔ 2.Реализовать метод в square для оставшихся фигур (Triangle+Parallelogram)
# ✔ 3.Для того, чтобы печатать цветной текст в терминале с помощью print можно использовать
#   т.н. эскейп-последовательности (escape sequences): https://www.skillsugar.com/how-to-print-coloured-text-in-python .
#   Нужный цвет "включается" с помощью распечатки определенной строки и выключается также.
#   Создайте контекстный менеджер colorizer, который будет печатать заданным цветом в произвольном блоке кода.
#   После выхода из блока текст печатается обычным образом:
# ✔ 4.В Питоне нет класса frange, который бы работал с float. Создать свою версию такого класса, который бы поддерживал
#   интерфейс стандартного range, но работал при этом с float.
# ✔ 5.Реализовать задание 6.5 таким образом, чтобы для проверки вхождения точки в окружность вместо вызова метода
#   contains можно было написать: p in c


from math import pi
from colorama import Fore


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)


class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.r = radius

    def __contains__(self, p: Point):  # (x - x0)^2 + (y - y0)^2 <= R^2
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2 <= self.r ** 2

    def square(self):
        return pi * self.r ** 2


class Triangle:
    def __init__(self, first_point: Point, second_point: Point, third_point: Point):
        self.A = first_point
        self.B = second_point
        self.C = third_point

    def square(self):  # S{ABC} = 1/2*( (x_2-x_1)*(y_3-y_1) - (x_3-x_1)*(y_2-y_1) )
        return abs(((self.B.x - self.A.x) * (self.C.y - self.A.y) - (self.C.x - self.A.x) * (self.B.y - self.A.y)) / 2)


class Parallelogram:
    def __init__(self, first_point: Point, second_point: Point, third_point: Point, fourth_point: Point):
        self.A = first_point
        self.B = second_point
        self.C = third_point
        self.D = fourth_point

    def square(self):  # S{ABCD} = (d_2-a_2) * (b_1-a_1)
        return abs((self.D.y - self.A.y) * (self.B.x - self.A.x))


class colorizer:
    def __init__(self, color='WHITE'):
        self.color = color.upper()

    def __enter__(self):
        __colors = {'BLACK': Fore.BLACK,
                    'RED': Fore.RED,
                    'GREEN': Fore.GREEN,
                    'YELLOW': Fore.YELLOW,
                    'BLUE': Fore.BLUE,
                    'MAGENTA': Fore.MAGENTA,
                    'CYAN': Fore.CYAN,
                    'WHITE': Fore.WHITE}
        color = __colors.get(self.color)
        if color:
            print(color)  # Activate color mode
        else:
            raise Exception('No such color')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Fore.RESET)  # Disactivate CM


class frange:
    def __init__(self, stop, start=None, step=1):
        self.stop = stop  # 1 arg passed
        if start is not None:  # 2 args passed
            self.start = stop
            self.stop = start
        else:  # 1 arg passed so default value
            self.start = 0
        self.step = step  # if 3 args passed, else = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.step > 0:  # Step validation
            if self.start + self.step >= self.stop + self.step:  # Check if limit was exceeded
                raise StopIteration
        elif self.step < 0:
            if self.start + self.step <= self.stop + self.step:
                raise StopIteration
        elif self.step == 0:
            raise ValueError('frange() arg 3 must not be zero')
        
        res = self.start  # Remember the value before increasing
        self.start += self.step  # Increasing
        return res
