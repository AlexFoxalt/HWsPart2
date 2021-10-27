from random import randint, choice

from django.db import models
from django.urls import reverse

from services.services_constants import FAKER
from services.services_functions import generate_random_student_avatar, get_data_from_file_in_str_format
from users.models import User, Course


class Student(User):
    photo = models.ImageField(upload_to='user_photo/student/',
                              verbose_name='Photo',
                              default=generate_random_student_avatar())
    resume = models.FileField(upload_to='user_resume/student/',
                              verbose_name='Resume',
                              default='default_resume/no_resume.png')
    previous_educational_institution = models.CharField(max_length=100, null=True, default='-',
                                                        verbose_name='Previous educational institution')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='Course')
    invited = models.IntegerField(default=0, verbose_name='Number of invited students')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def get_absolute_url(self):
        return reverse('student-profile', kwargs={'pk': self.pk})

    def increase_invitational_number(self):
        self.invited += 1
        self.save()

    def get_resume_in_template_format(self):
        ext = self.resume.url.rsplit('.')[1]
        path = self.resume.url[1:]
        return get_data_from_file_in_str_format(path, ext)

    @classmethod
    def _extend_fields(cls, data):
        data.update({
            'birthday': FAKER.date_between(start_date='-50y', end_date='-16y'),
            'position': 'Student',
            'previous_educational_institution': f'School №{randint(1, 100)}',
            'course': choice(Course.objects.all()),
            'photo': generate_random_student_avatar()
        })

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)

    def get_fields_for_displaying_user_in_list(self):
        return super().get_fields_for_displaying_user_in_list() + [self.photo, self.resume]

    @classmethod
    def get_columns_for_displaying_user_in_list(cls):
        return super().get_columns_for_displaying_user_in_list() + [cls.photo.field.verbose_name,
                                                                    cls.resume.field.verbose_name]
