from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User, Student, Teacher
from .utils import faculties_selector, positions_selector


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'birthday', 'email', 'phone_number', 'faculty', 'position']
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=faculties_selector),
            'position': forms.Select(choices=positions_selector),
        }

    def clean_email(self):
        invalid_domain_names = ('@abc.com', '@123.com', '@xyz.com')
        email = self.cleaned_data['email']

        for domain_name in invalid_domain_names:
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


# Next 2 classes added just for HW11/HW12 TechTask


class CreateTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1))
        }

    def clean(self):
        cleaned_data = super().clean()
        experience_in_years = cleaned_data.get('experience_in_years')
        birthday = cleaned_data.get('birthday')

        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if age <= experience_in_years:
            self.add_error('experience_in_years', 'Can not be greater then Age!')
            self.add_error('birthday', 'Can not be less then Exp!')
            raise ValidationError('How can it be???', code='invalid')

        return cleaned_data


class CreateStudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Student
        fields = '__all__'


# -------------------------------------------


class EditStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=faculties_selector),
            'position': forms.Select(choices=positions_selector),
        }


class EditTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=faculties_selector),
            'position': forms.Select(choices=positions_selector),
            'date_of_employment': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1))
        }