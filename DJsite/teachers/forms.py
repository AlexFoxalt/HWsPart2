from django import forms
from django.forms import ModelForm

from datetime import datetime

from services.services_constants import FACULTIES_SELECTOR, TEACHER_REQUIRED_FOR_FILLING_FIELDS
from teachers.models import Teacher


class EditTeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.initial_text = 'currently---'
        self.fields['photo'].widget.input_text = 'change------'

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ('position', 'user', 'filled')
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=FACULTIES_SELECTOR),
            'date_of_employment': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
        }


class RegisterTeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in TEACHER_REQUIRED_FOR_FILLING_FIELDS:
            self.fields[field].required = True

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            self.instance.filled = True  # Activating user after filling all additional fields
            self.instance.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance

    save.alters_data = True

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ('position', 'user', 'filled')
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380123456789'}),
            'faculty': forms.Select(choices=FACULTIES_SELECTOR),
            'date_of_employment': forms.SelectDateWidget(years=range(datetime.today().year, 1900, -1)),
        }
