from random import sample, randint

import django
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from services.services_generators import create_random_user, create_random_profile_data
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'),
        unique=True,
        help_text=_('Required. String in email format. Invisible for all users. Ex. i_like@python.com'),
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    nickname = models.CharField(
        _('Nickname'),
        max_length=50,
        unique=True,
        help_text=_('Required. Nickname on site. Visible for all users.'),
        error_messages={
            'unique': _("A user with that nickname already exists."),
        }
    )
    first_name = models.CharField(_('First Name'), max_length=150, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Person(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=100, null=True, verbose_name='City')
    birthday = models.DateField(null=True, verbose_name='Birthday')
    phone_number = models.CharField(max_length=50, null=True, unique=True, verbose_name='Phone number')
    faculty = models.CharField(max_length=255, default='not chosen', verbose_name='Faculty')
    position = models.CharField(max_length=255, default='not chosen', verbose_name='Position')
    filled = models.BooleanField(default=False, verbose_name='Filled status')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    @classmethod
    def generate_entity(cls, count):
        for _ in range(count):
            user = create_random_user(cls.__name__)
            profile_data = create_random_profile_data(user)

            cls._extend_fields(profile_data)

            if user._position == 'Teacher':
                profile = cls.objects.filter(user=user)

                courses = Course.objects.all()
                random_courses = sample(list(courses), randint(1, len(courses)))

                profile.update(**profile_data)
                profile[0].courses.set(random_courses)
                continue

            profile = cls.objects.filter(user=user)
            profile.update(**profile_data)

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
        return [self.user.first_name, self.user.last_name, self.user.nickname, self.position]

    def get_fields_for_displaying_user_in_search(self):
        return [self.user.first_name,
                self.user.last_name,
                self.city,
                self.birthday,
                self.faculty]

    @classmethod
    def get_columns_for_displaying_user_in_list(cls):
        return [get_user_model().first_name.field.verbose_name,
                get_user_model().last_name.field.verbose_name,
                get_user_model().nickname.field.verbose_name,
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
        no_objects_return = [('---', '---')]
        try:
            res = [(obj.pk, obj.name) for obj in cls.objects.all()]
        except django.db.utils.OperationalError:
            return no_objects_return

        return res if res else no_objects_return
