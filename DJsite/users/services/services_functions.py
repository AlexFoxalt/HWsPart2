from random import choice

from users.services.services_constants import FACULTIES


def mine_faker_of_faculties():
    return choice(FACULTIES)


def format_raw_cleaned_form_for_student(form):
    form.cleaned_data.pop('date_of_employment')
    form.cleaned_data.pop('experience_in_years')
    form.cleaned_data.pop('teacher_courses')


def format_raw_cleaned_form_for_teacher(form):
    form.cleaned_data.pop('teacher_courses')
    form.cleaned_data.pop('previous_educational_institution')
    form.cleaned_data.pop('student_course')


def combine_context(cont1, cont2):
    return dict(**cont1, **cont2)


def from_dict_to_list_of_dicts_format(arg: dict):
    return list({'field': field, 'value': value} for field, value in arg.items())
