from random import sample, randint

import django
from django.contrib.auth.models import User
from django.db import models

from services.services_generators import create_random_user, create_random_profile_data


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=100, null=True, verbose_name='City')
    birthday = models.DateField(null=True, verbose_name='Birthday')
    phone_number = models.CharField(max_length=50, null=True, unique=True, verbose_name='Phone number')
    faculty = models.CharField(max_length=255, default='not chosen', verbose_name='Faculty')
    position = models.CharField(max_length=255, default='not chosen', verbose_name='Position')
    filled = models.BooleanField(default=False, verbose_name='Filled information status')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    @classmethod
    def generate_entity(cls, count):
        for _ in range(count):
            user = create_random_user()
            profile_data = create_random_profile_data(user)

            cls._extend_fields(profile_data)

            if cls.__name__ == 'Teacher':
                courses = Course.objects.all()
                random_courses = sample(list(courses), randint(1, len(courses)))
                obj = cls.objects.create(**profile_data)
                obj.courses.set(random_courses)
                continue

            cls.objects.create(**profile_data)

    def __iter__(self):
        return self

    def __next__(self):
        field_names = [f.get_attname() for f in self.__class__._meta.fields]
        end = len(field_names)

        if self.counter >= end:
            raise StopIteration

        field_object = self.__class__._meta.get_field(field_names[self.counter])
        field_value = field_object.value_from_object(self)
        if str(field_object) == 'students.Student.course':
            course = Course.objects.get(pk=field_value)
            field_value = course.name

        self.counter += 1
        return field_value

    def get_fields_for_displaying_user_in_list(self):
        return [self.user.first_name, self.user.last_name, self.user.email, self.position]

    def get_fields_for_displaying_user_in_search(self):
        return [self.user.first_name,
                self.user.last_name,
                self.city,
                self.birthday,
                self.faculty]

    @classmethod
    def get_columns_for_displaying_user_in_list(cls):
        return [User.first_name.field.verbose_name,
                User.last_name.field.verbose_name,
                User.email.field.verbose_name,
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
