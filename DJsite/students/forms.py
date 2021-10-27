from datetime import datetime

from django import forms
from django.forms import ModelForm

from services.services_constants import FACULTIES_SELECTOR, POSITIONS_SELECTOR
from students.models import Student


class EditStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=FACULTIES_SELECTOR),
            'position': forms.Select(choices=POSITIONS_SELECTOR),
        }