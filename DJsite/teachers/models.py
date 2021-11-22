from django.db import models
from django.urls import reverse

from datetime import datetime
from random import randint, sample

from services.services_constants import FAKER
from users.models import Person, Course


class Teacher(Person):
    photo = models.ImageField(upload_to='user_photo/teacher/',
                              verbose_name='Photo',
                              default='default_avatar/teacher_avatar.png')
    date_of_employment = models.DateField(null=True, default=datetime.now, verbose_name='Date of employment')
    experience_in_years = models.IntegerField(null=True, default=0, verbose_name='Experience in years')
    courses = models.ManyToManyField(Course, verbose_name='Course')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def get_absolute_url(self):
        return reverse('teacher-profile', kwargs={'pk': self.pk})

    def get_teacher_courses(self):
        ret = []
        # models.ManyToMany field's all() return all the Course     objects that this user belongs to
        for course in self.courses.all():
            ret.append(course.name)
        return ret  # return list ob courses names

    @classmethod
    def _extend_fields(cls, data):
        data.update({
            'birthday': FAKER.date_between(start_date='-70y', end_date='-25y'),
            'position': 'Teacher',
            'date_of_employment': FAKER.date_between(start_date='-30y', end_date='today'),
            'experience_in_years': randint(1, 30)
        })

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)

    def get_fields_for_displaying_user_in_list(self):
        return super().get_fields_for_displaying_user_in_list() + [self.photo]

    def get_fields_for_displaying_user_in_search(self):
        return super().get_fields_for_displaying_user_in_search() + [self.date_of_employment,
                                                                     self.experience_in_years]

    @classmethod
    def get_columns_for_displaying_user_in_list(cls):
        return super().get_columns_for_displaying_user_in_list() + [cls.photo.field.verbose_name]
