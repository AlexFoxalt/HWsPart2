from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from webargs import djangoparser
from webargs.djangoparser import use_args

from services.services_constants import GET_INT_COUNT, TEACHER_FILTER_QUERY
from services.services_mixins import EntitySearchPerOneFieldMixin, EntityGeneratorMixin, GetAllUsersMixin, \
    EditUserMixin, DeleteUserMixin, ProfileMixin
from teachers.forms import EditTeacherForm
from teachers.models import Teacher

parser = djangoparser.DjangoParser()


class TeacherGenerator(EntityGeneratorMixin, LoginRequiredMixin, ListView):
    model = Teacher
    user_class = 'Teacher(s)'
    login_url = 'login'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)


class GetTeachers(EntitySearchPerOneFieldMixin, LoginRequiredMixin, ListView):
    model = Teacher
    login_url = 'login'

    @use_args(TEACHER_FILTER_QUERY, location='query')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetAllTeachers(LoginRequiredMixin, GetAllUsersMixin):
    model = Teacher
    template_name = 'main/list_of_users.html'
    page_id = 2
    login_url = 'login'


class EditTeacher(LoginRequiredMixin, EditUserMixin):
    form_class = EditTeacherForm
    model = Teacher
    page_id = 6
    login_url = 'login'


class DeleteTeacher(LoginRequiredMixin, DeleteUserMixin):
    model = Teacher
    page_id = 8
    login_url = 'login'


class TeacherProfile(LoginRequiredMixin, ProfileMixin):
    model = Teacher
    page_id = 11
    login_url = 'login'
