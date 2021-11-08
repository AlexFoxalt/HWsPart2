"""All possible util functions that DON'T need any project imports except CONSTANTS"""
import ast
from random import choice, randint
from typing import Union

import docx
from PyPDF2 import PdfFileReader

from services.services_constants import FACULTIES
from users.tokens import AccountActivationTokenGenerator


def mine_faker_of_faculties() -> str:
    return choice(FACULTIES)


def format_raw_cleaned_data_for_user(form, keys_to_pop) -> None:
    for key in keys_to_pop:
        form.cleaned_data.pop(key)
    # If user did not set photo or resume in reg.form just remove them, it'll be set automatically by model
    form.cleaned_data.pop('photo') if not form.cleaned_data['photo'] else None
    form.cleaned_data.pop('resume') if not form.cleaned_data['resume'] else None


def combine_context(cont1: dict, cont2: dict) -> dict:
    return dict(**cont1, **cont2)


def from_dict_to_list_of_dicts_format(arg: dict) -> list:
    return list({'field': field, 'value': value} for field, value in arg.items())


def get_position_from_cleaned_data(form) -> str:
    return form.cleaned_data.get('position', None)


def set_cleaned_data_value_to_list_of_objects(form, value, cls):
    form.cleaned_data[value] = cls.objects.get(pk=form.cleaned_data[value])


def get_list_of_objects_from_cleaned_data(form, key) -> list:
    value_as_str = form.cleaned_data.get(key)
    return ast.literal_eval(value_as_str)


def get_objects_by_list(cls, courses: list):
    return cls.objects.filter(pk__in=courses)


def generate_random_student_avatar():
    num = randint(1, 15)
    return f'default_avatar/student_avatar{num}.png'


def release_invitational_system(form, position):
    inviter = form.cleaned_data.get('invited_by', None)
    if inviter:
        user = position.objects.get(email=inviter)
        user.increase_invitational_number()


def read_txt_file(path) -> Union[str, None]:
    try:
        with open(path, 'r') as file:
            res = file.read()
        return res
    except:
        return None


def read_docx_file(path) -> Union[str, None]:
    try:
        doc = docx.Document(path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except:
        return None


def read_pdf_file(path) -> Union[str, None]:
    try:
        reader = PdfFileReader(path)
        pageObj = reader.getNumPages()
        text = []
        for page_count in range(pageObj):
            page = reader.getPage(page_count)
            text.append(page.extractText())
        return '\n'.join(text)
    except:
        return None


def get_data_from_file_in_str_format(path, extension) -> str:
    if extension == 'txt':
        res = read_txt_file(path)
    elif extension == 'docx':
        res = read_docx_file(path)
    elif extension == 'pdf':
        res = read_pdf_file(path)
    else:
        res = None

    return res if res else 'Something went wrong while reading this file :('


def get_pos_and_course_from_args(args):
    return args[0].get('pos', None), args[0].get('course', None)


def set_path(filename):
    return f'authentication/password/{filename}'


def check_and_activate_current_user(current_user, token):
    if current_user and AccountActivationTokenGenerator().check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        return True
    return False


def get_profile_columns_for_class(cls, columns):
    if cls.__name__ == 'User':
        return [f.verbose_name for f in cls._meta.fields
                if f.verbose_name in columns]
    return [f.verbose_name for f in cls.model._meta.fields
            if f.verbose_name in columns]
