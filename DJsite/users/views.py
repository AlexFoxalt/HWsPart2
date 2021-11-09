from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import BadRequest
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch, reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, RedirectView
from webargs.djangoparser import use_args

import users
from services.services_constants import POSITION_AND_COURSE_FILTER_QUERY, parser
from services.services_emails import send_registration_email
from services.services_error_handlers import page_not_found, forbidden_error
from services.services_functions import combine_context, get_position_from_cleaned_data, \
    get_pos_and_course_from_args, check_and_activate_current_user
from services.services_mixins import ContextMixin, StaffPermissionAndLoginRequired, DeleteUserMixin
from services.services_models import get_users_by_pos_and_course, get_and_save_object_by_its_position, \
    get_model_name_by_pk, create_user_with_custom_fields, get_current_user_from_encoded_data, \
    check_if_courses_exists_and_create_if_not, get_user_by_pk
from users.forms import CreateUserForm, RegisterUserForm, LoginUserForm


class Home(ContextMixin, TemplateView):
    template_name = 'main/index.html'
    page_id = 1

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return render(request, self.template_name, context=combine_context(context, extra_context))


class About(ContextMixin, TemplateView):
    template_name = 'main/about.html'
    page_id = 15

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return render(request, self.template_name, context=combine_context(context, extra_context))


class Links(ContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'main/links.html'
    page_id = 16
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return render(request, self.template_name, context=combine_context(context, extra_context))


class CreateUser(ContextMixin, StaffPermissionAndLoginRequired, CreateView):
    form_class = CreateUserForm
    template_name = 'main/create_user.html'
    page_id = 4
    login_url = 'login'

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


class EditUser(LoginRequiredMixin, RedirectView):
    """
    Tech view for redirection, depending on chosen object's model
    """
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk != request.user.pk and not request.user.is_superuser:
            return forbidden_error(request, 'You can\'t edit profile, that doesn\'t belong to you')

        try:
            return redirect(f'edit-{get_model_name_by_pk(pk)}', pk=pk)
        except NoReverseMatch:
            return page_not_found(request, 'Position of user error, no such users!')


class DeleteUser(LoginRequiredMixin, DeleteUserMixin):
    model = get_user_model()
    page_id = 7
    login_url = 'login'


class GetUsersByCourse(ContextMixin, LoginRequiredMixin, TemplateView):
    template_name = "main/get-users-by-course.html"
    page_id = 10
    login_url = 'login'

    @use_args(POSITION_AND_COURSE_FILTER_QUERY, location='query')
    def get(self, request, *args, **kwargs):
        pos, course = get_pos_and_course_from_args(args)

        if pos is None or course is None:
            return page_not_found(request, 'Position or Course can not be NoneType. '
                                           'Maybe be you don\'t create a Course?')
        elif course == '---':
            return page_not_found(request, 'We didn\'t find any Course. Yoo can create it in admin panel')

        user_list, pos, course, columns = get_users_by_pos_and_course(pos, course)

        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id,
                                              posts=user_list,
                                              position=pos,
                                              course=course,
                                              columns=columns)
        return render(request, self.template_name, context=combine_context(context, extra_context))


class RegisterUser(ContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'authentication/register.html'
    page_id = 13

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return combine_context(context, extra_context)

    def form_valid(self, form):
        # Custom version of user = form.save(), because we need to pass some extra arguments to signal handler
        user = create_user_with_custom_fields(form)

        send_registration_email(request=self.request,
                                user_instance=user)
        messages.success(self.request, f'Email sent! Waiting for activation...')
        return redirect('users-home')


class ActivateUser(RedirectView):
    def get(self, request, uidb64, token, *args, **kwargs):
        current_user = get_current_user_from_encoded_data(uidb64)
        status = check_and_activate_current_user(current_user, token)

        if status:
            login(request, current_user)
            messages.success(self.request, f'Verification complete! Now please enter additional info')
            return redirect(reverse('register-next-step',
                                    kwargs={'pk': current_user.pk}))
        else:
            messages.error(self.request, f'This account is already activated!')
            return redirect(reverse_lazy('users-home'))


class UserContinuedRegistration(LoginRequiredMixin, RedirectView):
    """
    Tech view for redirection, depending on chosen object's model
    """
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        # If it is first launch, we have no courses for registration. Let's create them
        check_if_courses_exists_and_create_if_not()

        pk = kwargs.get("pk")
        try:
            return redirect(f'{get_model_name_by_pk(pk)}/')
        except NoReverseMatch:
            return page_not_found(request, 'Position of user error, no such users!')


class LoginUser(ContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'
    page_id = 14

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return combine_context(context, extra_context)

    def get_success_url(self):
        return reverse_lazy('users-home')


class LogoutUser(LogoutView):
    next_page = 'users-home'


class UserProfile(LoginRequiredMixin, RedirectView):
    """
    Tech view for redirection, depending on chosen object's model
    """
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        try:
            user = get_user_by_pk(kwargs.get("pk"))
            return redirect(f'{user.position.lower()}-profile', pk=user.pk)
        except NoReverseMatch:
            return page_not_found(request, 'Position of user error, no such users!')
        except AttributeError:
            return page_not_found(request, 'User has no position. Maybe you are an admin? '
                                           'Admins have not yet come up with a profile :)')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error parser for webargs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)
