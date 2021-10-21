"""All possible util functions that DON'T need any project imports"""
import ast
from random import choice

from users.services.services_constants import FACULTIES


def mine_faker_of_faculties() -> str:
    return choice(FACULTIES)


def format_raw_cleaned_data_for_student(form) -> None:
    form.cleaned_data.pop('date_of_employment')
    form.cleaned_data.pop('experience_in_years')
    form.cleaned_data.pop('teacher_courses')


def format_raw_cleaned_data_for_teacher(form) -> None:
    form.cleaned_data.pop('teacher_courses')
    form.cleaned_data.pop('previous_educational_institution')
    form.cleaned_data.pop('course')


def combine_context(cont1, cont2):
    return dict(**cont1, **cont2)


def from_dict_to_list_of_dicts_format(arg: dict) -> list:
    return list({'field': field, 'value': value} for field, value in arg.items())


def get_position_from_cleaned_data(form) -> str:
    return form.cleaned_data.get('position', None)


def set_cleaned_data_position_to(form, arg) -> None:
    form.cleaned_data['position'] = arg


def set_cleaned_data_value_to_list_of_objects(form, value, cls):
    form.cleaned_data[value] = cls.objects.get(pk=form.cleaned_data[value])


def get_list_of_objects_from_cleaned_data(form, key) -> list:
    value_as_str = form.cleaned_data.get(key)
    return ast.literal_eval(value_as_str)


def get_courses_by_class(cls, courses):
    return cls.objects.filter(pk__in=courses)
