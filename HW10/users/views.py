from django.http import HttpResponse
from django.shortcuts import render
from webargs.djangoparser import use_kwargs, use_args
from django.db.models import Q
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.views.generic import ListView, DetailView, TemplateView

from .utils import teacher_filter_query, student_filter_query, get_int_count, home_page_posts, EntityGeneratorMixin, \
    EntitySearchPerOneFieldMixin, EntitySearchPerAllFieldsMixin
from .models import Student, Teacher, User

# Create your views here.
parser = djangoparser.DjangoParser()


class StudentHome(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Main Page',
            'posts': home_page_posts
        }
        return render(request, self.template_name, context=context)


class StudentGenerator(EntityGeneratorMixin, ListView):
    model = Student

    @parser.use_kwargs(get_int_count, location="query")
    def get(self, request, count, *args, **kwargs):
        user_class = 'Student(s)'
        return super().get(request, count, user_class, *args, **kwargs)  # cls,request,count,args,kwargs


class TeacherGenerator(EntityGeneratorMixin, ListView):
    model = Teacher

    @parser.use_kwargs(get_int_count, location="query")
    def get(self, request, count, *args, **kwargs):
        user_class = 'Teacher(s)'
        return super().get(request, count, user_class, *args, **kwargs)


class GetAllTeachers(ListView):
    model = Teacher
    template_name = 'list_of_users.html'

    def get(self, request, *args, **kwargs):
        posts = Teacher.objects.all()
        context = {
            'title': 'All teachers',
            'user_class': 'Teacher(s)',
            'posts': posts
        }
        return render(request, self.template_name, context=context)


class GetAllStudents(ListView):
    model = Student
    template_name = 'list_of_users.html'

    def get(self, request, *args, **kwargs):
        posts = Student.objects.all()
        context = {
            'title': 'All students',
            'user_class': 'Student(s)',
            'posts': posts
        }
        return render(request, self.template_name, context=context)


class GetTeachers(EntitySearchPerOneFieldMixin, ListView):
    model = Teacher

    @use_args(teacher_filter_query, location='query')
    def get(self, request, *args, **kwargs):
        user_class = 'Teacher(s)'
        return super().get(request, user_class, *args, **kwargs)


class GetStudents(EntitySearchPerAllFieldsMixin, ListView):
    model = Student

    @use_args(student_filter_query, location='query')
    def get(self, request, text, *args, **kwargs):
        user_class = 'Students(s)'
        return super().get(request, user_class, text, *args, **kwargs)


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)
