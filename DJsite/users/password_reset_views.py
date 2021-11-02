from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from services.services_functions import set_path
from services.services_mixins import ContextMixin, PasswordResetMixin


class UsersPasswordResetView(PasswordResetMixin, ContextMixin, PasswordResetView):
    template_name = set_path('password_reset_form.html')
    html_email_template_name = set_path('password_reset_email.html')


class UsersPasswordResetDoneView(PasswordResetMixin, ContextMixin, PasswordResetDoneView):
    template_name = set_path('password_reset_sent.html')


class UsersPasswordResetConfirmView(PasswordResetMixin, ContextMixin, PasswordResetConfirmView):
    template_name = set_path('password_reset_confirm.html')


class UsersPasswordResetCompleteView(PasswordResetMixin, ContextMixin, PasswordResetCompleteView):
    template_name = set_path('password_reset_complete.html')
