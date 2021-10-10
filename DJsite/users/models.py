from django.db import models
from datetime import datetime
from random import randint
from faker import Faker

from .utils import mine_faker_of_faculties

f = Faker('EN')


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    birthday = models.DateField(null=False)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=50, null=False)
    faculty = models.CharField(max_length=255, default='not chosen')
    position = models.CharField(max_length=255, default='not chosen')
    time_create = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_entity(cls, count):
        for _ in range(count):
            data = {
                'first_name': f.first_name(),
                'last_name': f.last_name(),
                'city': f.city(),
                'email': f.email(),
                'phone_number': f.phone_number(),
                'faculty': mine_faker_of_faculties()
            }
            cls._extend_fields(data)
            cls.objects.create(**data)


class Teacher(User):
    date_of_employment = models.DateField(null=True, default=datetime.now)
    experience_in_years = models.IntegerField(null=True, default=0)

    @classmethod
    def _extend_fields(cls, data):
        data.update({
            'birthday': f.date_between(start_date='-70y', end_date='-25y'),
            'position': 'Teacher',
            'date_of_employment': f.date_between(start_date='-30y', end_date='today'),
            'experience_in_years': randint(1, 30)
        })

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)


class Student(User):
    previous_educational_institution = models.CharField(max_length=100, null=True, default='-')

    @classmethod
    def _extend_fields(cls, data):
        data.update({
            'birthday': f.date_between(start_date='-50y', end_date='-16y'),
            'position': 'Student',
            'previous_educational_institution': f'School №{randint(1, 100)}'
        })

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)
