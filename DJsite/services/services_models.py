"""Here we are working with stuff that need imports from models.py"""
from django.contrib.auth.models import User as U
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from students.models import Student
from teachers.models import Teacher
from users.models import Course, User
from services.services_constants import OPTIONS, HOME_PAGE_POSTS, POSITIONS_SELECTOR, KEYS_TO_POP_FOR_STUDENT, \
    KEYS_TO_POP_FOR_TEACHER
from services.services_functions import format_raw_cleaned_data_for_user, \
    set_cleaned_data_value_to_list_of_objects, get_list_of_objects_from_cleaned_data, get_objects_by_list, \
    release_invitational_system

CONTEXT_CONTAINER = {
    1: {'title': 'Main Page', 'selected': 1},
    2: {'title': 'All teachers', 'user_class': 'Teacher(s)'},
    3: {'title': 'All students', 'user_class': 'Student(s)'},
    4: {'title': 'Create User', 'url': 'create-user', 'options': OPTIONS},
    5: {'title': 'Edit Student', 'position': 'Student', 'url': 'delete-student'},
    6: {'title': 'Edit Teacher', 'position': 'Teacher', 'url': 'delete-teacher'},
    7: {'title': 'Delete Student', 'position': 'Student'},
    8: {'title': 'Delete Teacher', 'position': 'Teacher'},
    9: {'title': 'Create Teacher', 'url': 'create-teacher'},
    10: {'title': 'Users by course'},
    11: {'title': 'Student Profile'},
    12: {'title': 'Teacher Profile'},
    13: {'title': 'Register', 'selected': 5},
    14: {'title': 'Sign in', 'selected': 4},
    15: {'title': 'About', 'selected': 2},
    16: {'title': 'Links',
         'selected': 3,
         'posts': HOME_PAGE_POSTS,
         'fs_positions': POSITIONS_SELECTOR,
         'fs_courses': Course.get_all_objects_of_class_in_selector_format()},
    17: {'title': 'Register Student', 'position': 'Student'},
    18: {'title': 'Register Teacher', 'position': 'Teacher'},
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
    return User.objects.get(pk=pk).position.lower()


def get_user_by_username(username):
    user = U.objects.get(username=username)
    return User.objects.get(user=user)


def create_new_profile_by_position(instance):
    pos = instance._position
    if pos == 'Student':
        Student.objects.create(user=instance, position=pos)
    elif pos == 'Teacher':
        Teacher.objects.create(user=instance, position=pos)


def set_default_group_for_user(user):
    my_group = Group.objects.get(name='Client')
    my_group.user_set.add(user)


def create_user_with_custom_fields(form):
    data = form.cleaned_data
    newuser = U(
        username=data['username'],
        email=data['email']
    )
    newuser.set_password(data['password1'])
    newuser.is_active = False

    # Set some extra attrs to the instance to be used in the handler.
    newuser._position = data['position']

    newuser.save()
    set_default_group_for_user(newuser)
    return newuser


def check_if_profile_is_filled(user):
    user = User.objects.get(pk=user.pk)
    return user.filled


def get_user_groups(user):
    res = [None, ]
    for g in user.groups.all():
        res.append(g.name)
    return res


def get_initial_values_from_user(pk):
    user = U.objects.get(pk=pk)
    return {'first_name': user.first_name,
            'last_name': user.last_name}


def get_current_user_from_encoded_data(uidb64):
    try:
        user_pk = force_bytes(urlsafe_base64_decode(uidb64))
        current_user = U.objects.get(pk=user_pk)
    except (U.DoesNotExist, ValueError, TypeError):
        return None

    return current_user
