from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from services.services_constants import FACULTIES_SELECTOR, POSSIBLE_EXTENSIONS_FOR_PROFILE, INVALID_DOMAIN_NAMES, \
    POSITIONS_SELECTOR
from students.models import Student
from users.models import Course, Person


class ExtendingUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CreateUserForm(ModelForm):
    photo = forms.ImageField(label='Photo',
                             required=False)
    date_of_employment = forms.DateField(label='Teacher\'s date of employment',
                                         required=False,
                                         widget=forms.SelectDateWidget(years=range(datetime.today().year, 1960, -1)))
    experience_in_years = forms.IntegerField(label='Teacher\'s experience in years',
                                             required=False,
                                             widget=forms.NumberInput(attrs={'value': 0}))
    previous_educational_institution = forms.CharField(label='Student\'s previous educational institution',
                                                       required=False)
    course = forms.CharField(label='Student\'s course',
                             required=False,
                             widget=forms.Select(
                                 choices=Course.get_all_objects_of_class_in_selector_format()))
    teacher_courses = forms.CharField(label='Teacher\'s courses',
                                      required=False,
                                      widget=forms.SelectMultiple(
                                          choices=Course.get_all_objects_of_class_in_selector_format()))
    resume = forms.FileField(label='Student\'s resume',
                             required=False,
                             widget=forms.ClearableFileInput())
    invited_by = forms.CharField(label='Student\'s email invited by',
                                 required=False,
                                 widget=forms.EmailInput(attrs={'placeholder': 'user_that@invite.you'}))

    class Meta:
        model = Person
        fields = ['city', 'birthday', 'phone_number', 'faculty', 'position']
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=FACULTIES_SELECTOR),
            'position': forms.Select(choices=POSITIONS_SELECTOR, attrs={'onchange': "showDiv(this)"}),
        }

    def clean_invited_by(self):
        inviter = self.cleaned_data['invited_by']
        if inviter:
            status = Student.objects.filter(email=self.cleaned_data['invited_by']).exists()
            if not status:
                raise ValidationError('No such user!', code='invalid')
        return inviter

    def clean_resume(self):
        resume = self.cleaned_data['resume']
        if resume is not None:
            ext = resume.name.rsplit('.')[1]
            if ext not in POSSIBLE_EXTENSIONS_FOR_PROFILE:
                raise ValidationError('Invalid extension!', code='invalid')
        return resume

    def clean_email(self):
        email = self.cleaned_data['email']
        for domain_name in INVALID_DOMAIN_NAMES:
            if domain_name in email:
                raise ValidationError('Invalid domain name!', code='invalid')
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if age < 18:
            raise ValidationError('This site is 18+ only', code='invalid')
        return birthday

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            raise ValidationError('First and Last name cannot repeat', code='invalid')
        return cleaned_data


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    position = forms.ChoiceField(label='Position', choices=POSITIONS_SELECTOR)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'login-form'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'login-form'}))
