"""Here we are working with stuff that need imports from models.py"""
import django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from students.models import Student
from teachers.models import Teacher
from users.models import Course, Person, CustomUser
from services.services_constants import OPTIONS, HOME_PAGE_POSTS, POSITIONS_SELECTOR, KEYS_TO_POP_FOR_STUDENT, \
    KEYS_TO_POP_FOR_TEACHER, USER_COLUMN_NAMES_FOR_SEARCH_PAGE, STUDENT_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE, \
    TEACHER_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE
from services.services_functions import format_raw_cleaned_data_for_user, \
    set_cleaned_data_value_to_list_of_objects, get_list_of_objects_from_cleaned_data, get_objects_by_list, \
    release_invitational_system, get_profile_columns_for_class

CONTEXT_CONTAINER = {
    1: {'title': 'Main Page', 'selected': 1},
    2: {'title': 'All teachers', 'user_class': 'Teacher(s)'},
    3: {'title': 'All students', 'user_class': 'Student(s)'},
    4: {'title': 'Create User', 'url': 'create-user', 'options': OPTIONS},
    5: {'title': 'Edit Student', 'position': 'Student', 'url': 'delete-student'},
    6: {'title': 'Edit Teacher', 'position': 'Teacher', 'url': 'delete-teacher'},
    7: {'title': 'Delete User', 'position': 'User'},
    9: {'title': 'Create Teacher', 'url': 'create-teacher'},
    10: {'title': 'Users by course'},
    11: {'title': 'Teacher Profile'},
    12: {'title': 'Student Profile'},
    13: {'title': 'Register', 'selected': 5},
    14: {'title': 'Sign in', 'selected': 4},
    15: {'title': 'About', 'selected': 2},
    16: {'title': 'Links',
         'selected': 3,
         'posts': HOME_PAGE_POSTS,
         'fs_positions': POSITIONS_SELECTOR},
    17: {'title': 'Register Student', 'position': 'Student'},
    18: {'title': 'Register Teacher', 'position': 'Teacher'},
}


def get_users_by_pos_and_course(pos: str, course: str):
    user_columns = get_profile_columns_for_class(get_user_model(), USER_COLUMN_NAMES_FOR_SEARCH_PAGE)
    if pos == 'Student':
        course = Course.objects.get(pk=course)
        profile_columns = get_profile_columns_for_class(Student, STUDENT_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE)
        columns = user_columns + profile_columns
        return Student.objects.filter(course_id=course.pk), pos, course, columns
    elif pos == 'Teacher':
        course = Course.objects.get(pk=course)
        profile_columns = get_profile_columns_for_class(Teacher, TEACHER_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE)
        columns = user_columns + profile_columns
        return Teacher.objects.filter(courses=course.pk), pos, course, columns


def get_and_save_object_by_its_position(position: str, form):
    user_position = 'User'
    if position == 'Student':
        release_invitational_system(form, Student)
        format_raw_cleaned_data_for_user(form, KEYS_TO_POP_FOR_STUDENT)
        set_cleaned_data_value_to_list_of_objects(form, 'course', Course)

        Student.objects.create(**form.cleaned_data)
        user_position = 'Student'
    elif position == 'Teacher':
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


def get_model_name_by_pk(pk):
    return Person.objects.get(pk=pk).position.lower()


def get_user_by_pk(pk):
    user = get_user_model().objects.get(pk=pk)
    if user.is_staff:
        return user
    return Person.objects.get(user=user)


def create_new_profile_by_position(instance):
    try:
        pos = instance._position
    except AttributeError:
        Student.objects.create(user=instance, position='Student')
        return

    if pos == 'Student':
        Student.objects.create(user=instance, position=pos)
    elif pos == 'Teacher':
        Teacher.objects.create(user=instance, position=pos)


def set_default_group_for_user(user):
    try:
        my_group = Group.objects.get(name='Client')
    except django.contrib.auth.models.Group.DoesNotExist:
        client_group = Group.objects.create(name='Client')
        staff_group = Group.objects.create(name='Staff')
        my_group = client_group

    my_group.user_set.add(user)


def create_user_with_custom_fields(form):
    data = form.cleaned_data
    newuser = get_user_model()(
        email=data['email'],
        nickname=data['nickname']
    )
    newuser.set_password(data['password1'])
    newuser.is_active = False

    # Set some extra attrs to the instance to be used in the handler.
    newuser._position = data['position']

    newuser.save()
    set_default_group_for_user(newuser)

    return newuser


def check_if_profile_is_filled(user):
    user = Person.objects.get(pk=user.pk)
    return user.filled


def get_user_groups(user):
    res = [None, ]
    for g in user.groups.all():
        res.append(g.name)
    return res


def get_initial_values_from_user(pk):
    user = get_user_model().objects.get(pk=pk)
    return {'first_name': user.first_name,
            'last_name': user.last_name}


def get_current_user_from_encoded_data(uidb64):
    try:
        user_pk = force_bytes(urlsafe_base64_decode(uidb64))
        current_user = get_user_model().objects.get(pk=user_pk)
    except (get_user_model().DoesNotExist, ValueError, TypeError):
        return None

    return current_user


def check_if_courses_exists():
    return Course.objects.all().exists()


def create_courses_from_1st_to_5th():
    names = ('First', 'Second', 'Third', 'Fourth', 'Fifth')
    for name in names:
        Course.objects.create(name=name)


def check_if_courses_exists_and_create_if_not():
    status = check_if_courses_exists()
    if not status:
        create_courses_from_1st_to_5th()


def add_filters_for_user_fields(or_cond, text):
    text_fields = ('user__first_name', 'user__last_name')
    for field in text_fields:
        or_cond |= Q(**{'{}__contains'.format(field): text})
    return or_cond


def get_last_added_user():
    return CustomUser.objects.latest('id')


def get_role_of_user(user):
    if user.is_authenticated:
        if user.is_staff:
            return 'admin'
        else:
            return get_model_name_by_pk(user.pk)
    else:
        return 'anonymous'
