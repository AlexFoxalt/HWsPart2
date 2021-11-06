"""Here we are working with all types on Mixins that shall be imported to views.py"""

import django
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from students.forms import RegisterStudentForm, EditStudentForm
from students.models import Student
from teachers.forms import EditTeacherForm, RegisterTeacherForm
from teachers.models import Teacher
from services.services_constants import OPTIONS, MENU_FOR_LOGGED_USER, MENU_FOR_UNLOGGED_USER, \
    NO_PROFILE_ANCHOR_PAGE_TITLES
from services.services_error_handlers import page_not_found, forbidden_error
from services.services_functions import from_dict_to_list_of_dicts_format, combine_context
from services.services_models import CONTEXT_CONTAINER, check_if_profile_is_filled, get_user_groups, \
    get_initial_values_from_user
from users.forms import ExtendingUserForm


class EntityGeneratorMixin:
    model = None
    template_name = 'entity_generator.html'
    context_object_name = 'content'

    @classmethod
    def get(cls, request, count, user_class, *args, **kwargs):
        try:
            cls.model.generate_entity(count)
        except (IndexError, ValueError):
            return page_not_found(request, 'You should create at least 1 Course, if you want to use generator')

        posts = cls.model.objects.all().order_by('-id')[:count][::-1]

        context = {
            'title': f'{user_class} generator',
            'user_class': user_class,
            'posts': posts,
            'menu': MENU_FOR_LOGGED_USER
        }
        return render(request, cls.template_name, context=context)


class EntitySearchMixinBase:
    model = None
    template_name = 'search_of_users.html'
    context_object_name = 'content'

    @classmethod
    def get_context_data(cls, request):
        posts = cls.model.objects.all()
        class_name = cls.model.__name__
        columns = [f.verbose_name for f in cls.model._meta.fields]

        context = {
            'title': f'{class_name}s searching',
            'user_class': f'{class_name}(s)',
            'posts': posts,
            'menu': MENU_FOR_LOGGED_USER,
            'auth_buttons_ids': [4, 5, 7],
            'columns': columns
        }

        if not request.user.is_superuser:
            context['filled'] = check_if_profile_is_filled(request.user)
            context['groups'] = get_user_groups(request.user)
        elif request.user.is_superuser:
            context['groups'] = [None, 'Staff', 'Client', 'admin']

        return context


class EntitySearchPerOneFieldMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, *args, **kwargs):
        context = super().get_context_data(request)
        applied_filters = []
        searching_keys = args[0]

        for key, value in searching_keys.items():
            if value is not None and value:
                context['posts'] = context['posts'].filter(**{f'{key}__contains': value})
                applied_filters.append(f'{key} --- {value}')

        context['applied_filters'] = applied_filters
        context['searching_fields'] = from_dict_to_list_of_dicts_format(searching_keys)
        return render(request, 'main/search_of_users.html', context=context)


class EntitySearchPerAllFieldsMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, text, *args, **kwargs):
        context = super().get_context_data(request)
        ajax_filter = request.GET.get('text', None)

        searching_keys = ajax_filter if ajax_filter is not None else text['text']

        if searching_keys is not None:
            text_fields = [f.name for f in cls.model._meta.get_fields() if
                           isinstance(f, django.db.models.fields.CharField)]
            or_cond = Q()

            for field in text_fields:
                or_cond |= Q(**{'{}__contains'.format(field): searching_keys})

            context['posts'] = context['posts'].filter(or_cond)

        context['searching_fields'] = from_dict_to_list_of_dicts_format(text)

        if request.is_ajax():
            html = render_to_string(
                template_name="main/posts-results-partial.html",
                context=context
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'main/search_of_users.html', context=context)


class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['selected'] = 0
        context['no_profile_anchor'] = NO_PROFILE_ANCHOR_PAGE_TITLES

        try:
            page_id = kwargs['page_id']
        except KeyError:
            page_id = 'default'

        context['auth_buttons_ids'] = [4, 5, 7]

        if self.request.user.is_authenticated:
            context['menu'] = MENU_FOR_LOGGED_USER
            if not self.request.user.is_superuser:
                context['filled'] = check_if_profile_is_filled(self.request.user)
                context['groups'] = get_user_groups(self.request.user)
            elif self.request.user.is_superuser:
                context['groups'] = [None, 'Staff', 'Client', 'admin']
        else:
            context['menu'] = MENU_FOR_UNLOGGED_USER

        container = CONTEXT_CONTAINER.get(page_id, None)
        if container:
            context.update(container)
        return context


class GetAllUsersMixin(ContextMixin, ListView):
    def get(self, request, *args, **kwargs):
        posts = self.model.objects.filter(filled=True)
        half_len = len(posts) // 2
        left_side_posts = posts[:half_len]
        right_side_posts = posts[half_len:]
        columns = [column_name for column_name in self.model.get_columns_for_displaying_user_in_list()]
        context = self.get_user_context(page_id=self.page_id,
                                        left_side_posts=left_side_posts,
                                        right_side_posts=right_side_posts,
                                        columns=columns)
        return render(request, self.template_name, context=context)


class ProfileMixin(ContextMixin, DetailView):
    template_name = 'main/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return combine_context(context, extra_context)


class EditUserMixin(ContextMixin, UpdateView):
    template_name = 'main/edit_user.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk != request.user.pk and not request.user.is_superuser:
            return forbidden_error(request, 'You can\'t edit profile, that doesn\'t belong to you')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=self.kwargs['pk'])

        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.POST or None,
                                                      initial=get_initial_values_from_user(self.kwargs['pk']))

        return combine_context(context, extra_context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.position == 'Teacher':
            form1 = EditTeacherForm(request.POST, instance=self.object)
        elif self.object.position == 'Student':
            form1 = EditStudentForm(request.POST, instance=self.object)
        form2 = ExtendingUserForm(request.POST, instance=self.object.user)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

        if self.model is Teacher:
            messages.success(self.request, 'Teacher edited successfully')
        elif self.model is Student:
            messages.success(self.request, 'Student edited successfully')

        return super().post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('user-profile', args=[self.object.user.username])


class UserContinuedRegistrationMixin(ContextMixin, UpdateView):
    template_name = 'main/continued-registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=self.kwargs['pk'])

        if 'form2' not in context:
            context['form2'] = self.second_form_class

        return combine_context(context, extra_context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.position == 'Teacher':
            form1 = RegisterTeacherForm(request.POST, instance=self.object)
        elif self.object.position == 'Student':
            form1 = RegisterStudentForm(request.POST, instance=self.object)

        form2 = ExtendingUserForm(request.POST, instance=self.object.user)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

        if self.model is Teacher:
            messages.success(self.request, 'Teacher filled successfully')
        elif self.model is Student:
            messages.success(self.request, 'Student filled successfully')

        return super().post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('users-home')


class DeleteUserMixin(ContextMixin, DeleteView):
    template_name = 'main/delete_user.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']

        extra_context = self.get_user_context(page_id=self.page_id,
                                              pk=pk,
                                              user=get_object_or_404(self.model, pk=pk))
        return combine_context(context, extra_context)

    def get_success_url(self, *args, **kwargs):
        if self.model is Teacher:
            messages.success(self.request, 'Teacher deleted successfully')
            return reverse_lazy('get-all-teachers')
        elif self.model is Student:
            messages.success(self.request, 'Student deleted successfully')
            return reverse_lazy('get-all-students')


class PasswordResetMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context()
        return combine_context(context, extra_context)
