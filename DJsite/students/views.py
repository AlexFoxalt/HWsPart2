from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from webargs.djangoparser import use_args

from services.services_constants import GET_INT_COUNT, parser, STUDENT_FILTER_QUERY
from services.services_mixins import EntityGeneratorMixin, EntitySearchPerAllFieldsMixin, GetAllUsersMixin, \
    EditUserMixin, DeleteUserMixin, ProfileMixin
from students.forms import EditStudentForm
from students.models import Student


class StudentGenerator(EntityGeneratorMixin, LoginRequiredMixin, ListView):
    model = Student
    user_class = 'Student(s)'
    login_url = 'login'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)  # cls,request,count,args,kwargs


class GetStudents(EntitySearchPerAllFieldsMixin, LoginRequiredMixin, ListView):
    model = Student
    login_url = 'login'

    @use_args(STUDENT_FILTER_QUERY, location='query')
    def get(self, request, text, *args, **kwargs):
        return super().get(request, text, *args, **kwargs)


class GetAllStudents(LoginRequiredMixin, GetAllUsersMixin):
    model = Student
    template_name = 'main/list_of_users.html'
    page_id = 3
    login_url = 'login'


class EditStudent(LoginRequiredMixin, EditUserMixin):
    form_class = EditStudentForm
    model = Student
    page_id = 5
    login_url = 'login'


class DeleteStudent(LoginRequiredMixin, DeleteUserMixin):
    model = Student
    page_id = 7
    login_url = 'login'


class StudentProfile(LoginRequiredMixin, ProfileMixin):
    model = Student
    page_id = 12
    login_url = 'login'
