"""HW6 Чернышов Алексей [OOP part]"""


# ✔ 1.Создать в классе Circle (x, y, radius) булевый метод contains, который принимает в качестве параметра точку
#     (экземпляр класса Point (x, y)) и проверяет находится ли данная точка внутри окружности. Координаты центра
#     окружности и точки могут быть произвольными. Если точка попадает на окружность, то это считается вхождением.
# ✔ 2.Создать класс Robot и его потомков - классы SpotMini, Atlas и Handle. В родительском классе должно быть определен
#     конструктор и как минимум 3 атрибута и 1 метод. В классах-потомках должны быть добавлены минимум по 1 новому
#     методу и по 1 новому атрибуту.


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.r = radius

    def contains(self, p: Point):  # (x - x0)^2 + (y - y0)^2 <= R^2
        res = (p.x - self.x) ** 2 + (p.y - self.y) ** 2 <= self.r ** 2
        return res


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Robot:
    def __init__(self, name, model, weight):
        self.name = name
        self.model = model
        self.weight = weight

    def IntroduceYourself(self):
        return f'Hello human, my name is {self.name}\n' \
               f'Model type is a {self.model}\n' \
               f'And my weight is {self.weight} kg.\n'


class SpotMini(Robot):
    def __init__(self, name, model, weight, color):
        super().__init__(name, model, weight)
        self.color = color

    def WhatCanYouDo(self):
        return f'I am robo-dog, i can do some cool tricks like a real dog.\n' \
               f'For example my color is {self.color}\n'


class Atlas(Robot):
    def __init__(self, name, model, weight, speed):
        super().__init__(name, model, weight)
        self.speed = speed

    def WhatCanYouDo(self):
        return f'I am robo-human, i can do some cool tricks like a real human.\n' \
               f'For example my running speed is {self.speed} km/h\n'


class Handle(Robot):
    def __init__(self, name, model, weight, power):
        super().__init__(name, model, weight)
        self.power = power

    def WhatCanYouDo(self):
        return f'I am robo-worker, i can do some cool tricks like a real worker.\n' \
               f'For example i can grab huge items, because my power is {self.power}W\n'


r1 = Robot('Wall-e', 'Cartoon Robot', 30)
print(r1.IntroduceYourself())

s1 = SpotMini('Scooby Doo', 'German dog', 15, 'brown')
print(s1.WhatCanYouDo())
print(s1.IntroduceYourself())

a1 = Atlas('Jake', 'BD Robot mod.302-111', 89, 15)
print(a1.WhatCanYouDo())
print(a1.IntroduceYourself())

h1 = Handle('Idle Hand', 'Movie hand from 99s', 5, 900)
print(h1.WhatCanYouDo())
print(h1.IntroduceYourself())

