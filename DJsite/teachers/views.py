from django.views.generic import ListView
from webargs import djangoparser
from webargs.djangoparser import use_args

from services.services_constants import GET_INT_COUNT, TEACHER_FILTER_QUERY
from services.services_mixins import EntitySearchPerOneFieldMixin, EntityGeneratorMixin, GetAllUsersMixin, \
    EditUserMixin, DeleteUserMixin, ProfileMixin
from teachers.forms import EditTeacherForm
from teachers.models import Teacher

parser = djangoparser.DjangoParser()


class TeacherGenerator(EntityGeneratorMixin, ListView):
    model = Teacher
    user_class = 'Teacher(s)'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)


class GetTeachers(EntitySearchPerOneFieldMixin, ListView):
    model = Teacher

    @use_args(TEACHER_FILTER_QUERY, location='query')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetAllTeachers(GetAllUsersMixin):
    model = Teacher
    template_name = 'list_of_users.html'
    page_id = 2


class EditTeacher(EditUserMixin):
    form_class = EditTeacherForm
    model = Teacher
    page_id = 6


class DeleteTeacher(DeleteUserMixin):
    model = Teacher
    page_id = 8


class TeacherProfile(ProfileMixin):
    model = Teacher
    page_id = 11
