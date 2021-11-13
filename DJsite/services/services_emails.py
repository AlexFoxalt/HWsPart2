from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tokens import AccountActivationTokenGenerator


def send_registration_email(request, user_instance):
    mail_subject = "Activate your account"

    message = render_to_string('authentication/account_verification.html',
                               {'user': user_instance,
                                'domain': get_current_site(request).domain,
                                'protocol': 'http',
                                'uid': urlsafe_base64_encode(
                                    force_bytes(user_instance.pk)),
                                'token': AccountActivationTokenGenerator().make_token(
                                    user_instance)})

    email = EmailMessage(subject=mail_subject,
                         body=message,
                         to=[user_instance.email],
                         )
    email.content_subtype = 'html'
    email.send(fail_silently=False)
