from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, NoReverseMatch
from webargs.djangoparser import use_args
from webargs import djangoparser
from django.core.exceptions import BadRequest
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, View

from .forms import CreateUserForm, EditStudentForm, EditTeacherForm
from users.services.services_functions import combine_context, get_position_from_cleaned_data
from .models import Student, Teacher, User
from .services.services_constants import GET_INT_COUNT, TEACHER_FILTER_QUERY, STUDENT_FILTER_QUERY, \
    POSITION_AND_COURSE_FILTER_QUERY
from .services.services_error_handlers import page_not_found
from .services.services_mixins import ContextMixin, EntityGeneratorMixin, GetAllUsersMixin, \
    EntitySearchPerOneFieldMixin, EntitySearchPerAllFieldsMixin
from .services.services_models import get_users_by_pos_and_course, get_and_save_object_by_its_position

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
    user_class = 'Student(s)'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)  # cls,request,count,args,kwargs


class TeacherGenerator(EntityGeneratorMixin, ListView):
    model = Teacher
    user_class = 'Teacher(s)'

    @parser.use_kwargs(GET_INT_COUNT, location="query")
    def get(self, request, count, *args, **kwargs):
        return super().get(request, count, self.user_class, *args, **kwargs)


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

    @use_args(TEACHER_FILTER_QUERY, location='query')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetStudents(EntitySearchPerAllFieldsMixin, ListView):
    model = Student

    @use_args(STUDENT_FILTER_QUERY, location='query')
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
        position = get_position_from_cleaned_data(form)
        if not position:
            return page_not_found(self.request, 'Position can not be NoneType!')

        status, user_position = get_and_save_object_by_its_position(position, form)

        if status:
            messages.success(self.request, f'{user_position} added successfully!')
        else:
            messages.error(self.request, f'{user_position} was not added. Something went wrong :(')

        return redirect('create-user')


class EditUser(View):
    """Tech view for redirection, depending on chosen object's model"""

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        model_name = User.objects.get(pk=pk).position
        try:
            return redirect(f'edit-{model_name.lower()}', pk=pk)
        except NoReverseMatch:
            return page_not_found(request, 'Position of user error, no such users!')


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


class GetUsersByCourse(ContextMixin, TemplateView):
    template_name = "get-users-by-course.html"
    page_id = 10

    @use_args(POSITION_AND_COURSE_FILTER_QUERY, location='query')
    def get(self, request, *args, **kwargs):
        pos = args[0].get('pos', None)
        course = args[0].get('course', None)

        print(pos, course)

        if pos is None or course is None:
            return page_not_found(request, 'Position or Course can not be NoneType. '
                                           'Maybe be you don\'t create a Course?')
        elif course == '---':
            return page_not_found(request, 'We didn\'t find any Course. Yoo can create it in admin panel')

        user_list, pos, course, columns = get_users_by_pos_and_course(pos, course)

        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              user_list=user_list,
                                              position=pos,
                                              course=course,
                                              columns=columns)
        return render(request, self.template_name, context=combine_context(context, extra_context))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error parser for webargs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)
