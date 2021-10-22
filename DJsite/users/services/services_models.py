"""Here we are working with stuff that need import Models from models.py"""

from faker import Faker
from webargs import djangoparser

from users.models import Course, Teacher, Student
from users.services.services_constants import OPTIONS, HOME_PAGE_POSTS, POSITIONS_SELECTOR, KEYS_TO_POP_FOR_STUDENT, \
    KEYS_TO_POP_FOR_TEACHER
from users.services.services_functions import format_raw_cleaned_data_for_user, set_cleaned_data_position_to, \
    set_cleaned_data_value_to_list_of_objects, get_list_of_objects_from_cleaned_data, get_objects_by_list

parser = djangoparser.DjangoParser()
f = Faker('EN')

CONTEXT_CONTAINER = {
    1: {'title': 'Main Page', 'selected': 1, 'posts': HOME_PAGE_POSTS,
        'fs_positions': POSITIONS_SELECTOR, 'fs_courses': Course._get_all_objects_of_class_in_selector_format()},
    2: {'title': 'All teachers', 'user_class': 'Teacher(s)'},
    3: {'title': 'All students', 'user_class': 'Student(s)'},
    4: {'title': 'Create User', 'url': 'create-user', 'options': OPTIONS},
    5: {'title': 'Edit Student', 'position': 'Student', 'url': 'delete-student'},
    6: {'title': 'Edit Teacher', 'position': 'Teacher', 'url': 'delete-teacher'},
    7: {'title': 'Delete Student', 'position': 'Student'},
    8: {'title': 'Delete Teacher', 'position': 'Teacher'},
    9: {'title': 'Create Teacher', 'url': 'create-teacher'},
    10: {'title': 'Users by course'}
}


def get_users_by_pos_and_course(pos: str, course: str):
    if pos == 'Student':
        course = Course.objects.get(pk=course)
        columns = [f.get_attname() for f in Student._meta.fields]
        return Student.objects.filter(course_id=course.pk), pos, course, columns
    elif pos == 'Teacher':
        course = Course.objects.get(pk=course)
        columns = [f.get_attname() for f in Teacher._meta.fields]
        return Teacher.objects.filter(courses=course.pk), pos, course, columns


def get_and_save_object_by_its_position(position: str, form):
    user_position = 'User'
    if position == '0':
        set_cleaned_data_position_to(form, 'Student')
        format_raw_cleaned_data_for_user(form, KEYS_TO_POP_FOR_STUDENT)
        set_cleaned_data_value_to_list_of_objects(form, 'course', Course)

        Student.objects.create(**form.cleaned_data)
        user_position = 'Student'
    elif position == '1':
        set_cleaned_data_position_to(form, 'Teacher')
        # We want to save this data here
        courses = get_list_of_objects_from_cleaned_data(form, 'teacher_courses')
        # Cus here we need to delete 'teacher_courses' from cleaned data
        format_raw_cleaned_data_for_user(form, KEYS_TO_POP_FOR_TEACHER)

        obj = Teacher.objects.create(**form.cleaned_data)
        # Using saved courses for linking to Course model as Many2Many
        obj.courses.set(get_objects_by_list(Course, courses))
        user_position = 'Teacher'
    else:
        return False, user_position

    return True, user_position
