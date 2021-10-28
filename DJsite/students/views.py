from django.views.generic import ListView
from webargs.djangoparser import use_args

from services.services_constants import GET_INT_COUNT, parser, STUDENT_FILTER_QUERY
from services.services_mixins import EntityGeneratorMixin, EntitySearchPerAllFieldsMixin, GetAllUsersMixin, \
    EditUserMixin, DeleteUserMixin, ProfileMixin
from students.forms import EditStudentForm
from students.models import Student


class StudentGenerator(EntityGeneratorMixin, ListView):
    model = Student
    user_class = 'Student(s)'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)  # cls,request,count,args,kwargs


class GetStudents(EntitySearchPerAllFieldsMixin, ListView):
    model = Student

    @use_args(STUDENT_FILTER_QUERY, location='query')
    def get(self, request, text, *args, **kwargs):
        return super().get(request, text, *args, **kwargs)


class GetAllStudents(GetAllUsersMixin):
    model = Student
    template_name = 'list_of_users.html'
    page_id = 3


class EditStudent(EditUserMixin):
    form_class = EditStudentForm
    model = Student
    page_id = 5


class DeleteStudent(DeleteUserMixin):
    model = Student
    page_id = 7


class StudentProfile(ProfileMixin):
    model = Student
    page_id = 12
