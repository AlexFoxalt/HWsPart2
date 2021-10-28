from datetime import datetime

from django import forms
from django.forms import ModelForm

from services.services_constants import FACULTIES_SELECTOR
from students.models import Student


class EditStudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.initial_text = 'currently---'
        self.fields['photo'].widget.input_text = 'change------'

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('position',)
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=FACULTIES_SELECTOR),
        }
