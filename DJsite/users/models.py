from random import sample, randint

import django
from django.contrib.auth.models import User as U
from django.db import models

from services.services_constants import FAKER
from services.services_functions import mine_faker_of_faculties


class User(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=100, null=True, verbose_name='Last Name')
    city = models.CharField(max_length=100, null=True, verbose_name='City')
    birthday = models.DateField(null=True, verbose_name='Birthday')
    email = models.EmailField(null=True, unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=50, null=True, unique=True, verbose_name='Phone number')
    faculty = models.CharField(max_length=255, default='not chosen', verbose_name='Faculty')
    position = models.CharField(max_length=255, default='not chosen', verbose_name='Position')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    @classmethod
    def generate_entity(cls, count):
        for _ in range(count):
            data = {
                'first_name': FAKER.first_name(),
                'last_name': FAKER.last_name(),
                'city': FAKER.city(),
                'email': FAKER.email(),
                'phone_number': FAKER.phone_number(),
                'faculty': mine_faker_of_faculties()
            }
            cls._extend_fields(data)

            if cls.__name__ == 'Teacher':
                random_courses = sample(list(Course.objects.all()), randint(1, 5))
                obj = cls.objects.create(**data)
                obj.courses.set(random_courses)
                continue

            cls.objects.create(**data)

    def __iter__(self):
        return self

    def __next__(self):
        field_names = [f.get_attname() for f in self.__class__._meta.fields]
        end = len(field_names)

        if self.counter >= end:
            raise StopIteration

        field_object = self.__class__._meta.get_field(field_names[self.counter])
        if str(field_object) == 'students.Student.course':
            field_value = field_object.value_from_object(self)
            course = Course.objects.get(pk=field_value)
            field_value = course.name
        else:
            field_value = field_object.value_from_object(self)

        self.counter += 1
        return field_value

    def get_fields_for_displaying_user_in_list(self):
        return [self.first_name, self.last_name, self.email, self.position]

    @classmethod
    def get_columns_for_displaying_user_in_list(cls):
        return [cls.first_name.field.verbose_name,
                cls.last_name.field.verbose_name,
                cls.email.field.verbose_name,
                cls.position.field.verbose_name]


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name

    @classmethod
    def get_all_objects_of_class_in_selector_format(cls):
        try:
            return [(obj.pk, obj.name) for obj in cls.objects.all()]
        except django.db.utils.OperationalError:
            return [('---', '---')]
