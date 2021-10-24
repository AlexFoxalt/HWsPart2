import django
from django.db import models

from datetime import datetime
from random import randint, choice, sample

from django.urls import reverse
from faker import Faker

from users.services.services_functions import mine_faker_of_faculties, generate_random_student_avatar

f = Faker('EN')


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100, null=False, verbose_name='First Name')
    last_name = models.CharField(max_length=100, null=False, verbose_name='Last Name')
    city = models.CharField(max_length=100, null=False, verbose_name='City')
    birthday = models.DateField(null=False, verbose_name='Birthday')
    email = models.EmailField(null=False, unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=50, null=False, unique=True, verbose_name='Phone number')
    faculty = models.CharField(max_length=255, default='not chosen', verbose_name='Faculty')
    position = models.CharField(max_length=255, default='not chosen', verbose_name='Position')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')

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
                'first_name': f.first_name(),
                'last_name': f.last_name(),
                'city': f.city(),
                'email': f.email(),
                'phone_number': f.phone_number(),
                'faculty': mine_faker_of_faculties()
            }
            cls._extend_fields(data)

            if cls == Teacher:
                random_courses = sample(list(Course.objects.all()), randint(1, 5))
                obj = Teacher.objects.create(**data)
                obj.courses.set(random_courses)
                continue

            print("!!!!!!!!!!!!", data)
            cls.objects.create(**data)


    def __iter__(self):
        return self

    def __next__(self):
        field_names = [f.get_attname() for f in self.__class__._meta.fields]
        end = len(field_names)

        if self.counter >= end:
            raise StopIteration

        field_object = self.__class__._meta.get_field(field_names[self.counter])
        field_value = field_object.value_from_object(self)
        self.counter += 1
        return field_value


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


class Teacher(User):
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
            'birthday': f.date_between(start_date='-70y', end_date='-25y'),
            'position': 'Teacher',
            'date_of_employment': f.date_between(start_date='-30y', end_date='today'),
            'experience_in_years': randint(1, 30),
        })

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' --- '.join(field_values)


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

    @classmethod
    def _extend_fields(cls, data):
        data.update({
            'birthday': f.date_between(start_date='-50y', end_date='-16y'),
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
