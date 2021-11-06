from django.test import TestCase

# Create your tests here.
from django.views.generic import TemplateView

from services.services_functions import set_path


class TestResetFormEmail(TemplateView):
    template_name = set_path('password_reset_email.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'TestTest'
        return context
