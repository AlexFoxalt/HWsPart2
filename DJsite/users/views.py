from django.contrib import messages
from django.shortcuts import render, redirect
from webargs.djangoparser import use_args
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.views.generic import ListView, TemplateView, CreateView

from .forms import CreateUserForm, CreateTeacherForm, CreateStudentForm
from .utils import teacher_filter_query, student_filter_query, get_int_count, home_page_posts, EntityGeneratorMixin, \
    EntitySearchPerOneFieldMixin, EntitySearchPerAllFieldsMixin
from .models import Student, Teacher

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


class CreateUser(CreateView):
    form_class = CreateUserForm
    template_name = 'create_user.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create User'
        return context

    def form_valid(self, form):
        position = form.cleaned_data['position']
        if position == 'Student':
            Student.objects.create(**form.cleaned_data)
            messages.success(self.request, 'Student added successfully!')
        elif position == 'Teacher':
            Teacher.objects.create(**form.cleaned_data)
            messages.success(self.request, 'Teacher added successfully!')
        else:
            messages.error(self.request, 'User was not added. Something went wrong :(')
        return redirect('create-user')

# Next 2 classes added just for HW11 TechTask ---------------------


class CreateTeacher(CreateView):
    form_class = CreateTeacherForm
    template_name = 'create_user.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Teacher'
        return context


class CreateStudent(CreateView):
    form_class = CreateStudentForm
    template_name = 'create_user.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Student'
        return context

# ------------------------------------------------------------------


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)
