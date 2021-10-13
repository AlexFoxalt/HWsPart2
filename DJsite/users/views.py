from django.contrib import messages
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from webargs.djangoparser import use_args
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, View

from .forms import CreateUserForm, EditStudentForm, EditTeacherForm
from .utils import teacher_filter_query, student_filter_query, get_int_count, EntityGeneratorMixin, \
    EntitySearchPerOneFieldMixin, EntitySearchPerAllFieldsMixin, ContextMixin, combine_context, GetAllUsersMixin
from .models import Student, Teacher, User

# Create your views here.
parser = djangoparser.DjangoParser()


class StudentHome(ContextMixin, TemplateView):
    template_name = 'index.html'
    page_id = 1

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return render(request, self.template_name, context=combine_context(context, extra_context))


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


class GetAllTeachers(GetAllUsersMixin):
    model = Teacher
    template_name = 'list_of_users.html'
    page_id = 2


class GetAllStudents(GetAllUsersMixin):
    model = Student
    template_name = 'list_of_users.html'
    page_id = 3


class GetTeachers(EntitySearchPerOneFieldMixin, ListView):
    model = Teacher

    @use_args(teacher_filter_query, location='query')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetStudents(EntitySearchPerAllFieldsMixin, ListView):
    model = Student

    @use_args(student_filter_query, location='query')
    def get(self, request, text, *args, **kwargs):
        return super().get(request, text, *args, **kwargs)


class CreateUser(ContextMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'create_user.html'
    page_id = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return combine_context(context, extra_context)

    def form_valid(self, form):
        position = form.cleaned_data['position']
        if position == '0':
            form.cleaned_data['position'] = 'Student'

            form.cleaned_data.pop('date_of_employment')
            form.cleaned_data.pop('experience_in_years')

            Student.objects.create(**form.cleaned_data)
            messages.success(self.request, 'Student added successfully!')
        elif position == '1':
            form.cleaned_data['position'] = 'Teacher'

            form.cleaned_data.pop('previous_educational_institution')

            Teacher.objects.create(**form.cleaned_data)
            messages.success(self.request, 'Teacher added successfully!')
        else:
            messages.error(self.request, 'User was not added. Something went wrong :(')

        return redirect('create-user')


class EditUser(View):
    """Tech view for redirection, depending on chosen object's model"""

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        model_name = User.objects.get(pk=pk).position
        return redirect(f'edit-{model_name.lower()}', pk=pk)


class EditStudent(ContextMixin, UpdateView):
    template_name = 'edit_user.html'
    form_class = EditStudentForm
    model = Student
    page_id = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=self.kwargs['pk'])
        return combine_context(context, extra_context)

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Student edited successfully')
        return result

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('edit-student', args=[str(self.kwargs['pk'])])


class EditTeacher(ContextMixin, UpdateView):
    template_name = 'edit_user.html'
    form_class = EditTeacherForm
    model = Teacher
    page_id = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=self.kwargs['pk'])
        return combine_context(context, extra_context)

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Teacher edited successfully')
        return result

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('edit-teacher', args=[str(self.kwargs['pk'])])


class DeleteStudent(ContextMixin, DeleteView):
    model = Student
    template_name = 'delete_user.html'
    page_id = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=pk,
                                              user=Student.objects.get(pk=pk))
        return combine_context(context, extra_context)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Student deleted successfully')
        return reverse_lazy('edit-student', args=[str(self.kwargs['pk'] + 1)])


class DeleteTeacher(ContextMixin, DeleteView):
    model = Teacher
    template_name = 'delete_user.html'
    page_id = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=pk,
                                              user=Teacher.objects.get(pk=pk))
        return combine_context(context, extra_context)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Teacher deleted successfully')
        return reverse_lazy('edit-teacher', args=[str(self.kwargs['pk'] + 1)])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error parsers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def page_not_found(request, exception):
    return render(request, '404.html')


def server_error(request):
    return HttpResponseServerError('<h1> 500 Server Error :( </h1>')
