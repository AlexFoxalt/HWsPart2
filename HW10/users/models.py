from django.db import models
from datetime import datetime
from .utils import mine_faker_of_faculties
from random import randint
from faker import Faker

f = Faker('EN')


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    birthday = models.DateField(null=False)
    email = models.EmailField(null=False)
    faculty = models.CharField(max_length=100, default=' - ')
    position = models.CharField(max_length=30, null=False)
    time_create = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_entity(cls, count):
        raise Exception('Unable to create base class entity')


class Teacher(User):
    date_of_employment = models.DateField(null=True, default=datetime.now)
    experience_in_years = models.IntegerField(null=False, default=0)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)

    @classmethod
    def generate_entity(cls, count):
        for iteration in range(count):
            data = {
                    'name': f.name(),
                    'city': f.city(),
                    'email': f.email(),
                    'faculty': mine_faker_of_faculties(),
                    'birthday': f.date_between(start_date='-70y', end_date='-25y'),
                    'position': 'Teacher',
                    'date_of_employment': f.date_between(start_date='-30y', end_date='today'),
                    'experience_in_years': randint(1, 30)
                }
            cls.objects.create(**data)


class Student(User):
    previous_educational_institution = models.CharField(max_length=100, null=False)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)

    @classmethod
    def generate_entity(cls, count):
        for iteration in range(count):
            data = {
                    'name': f.name(),
                    'city': f.city(),
                    'email': f.email(),
                    'faculty': mine_faker_of_faculties(),
                    'birthday': f.date_between(start_date='-50y', end_date='-16y'),
                    'position': 'Student',
                    'previous_educational_institution': f'School №{randint(1, 100)}'
                }
            cls.objects.create(**data)
