from django.http import HttpResponseServerError
from django.shortcuts import render

from services.services_functions import combine_context
from services.services_models import get_role_of_user

GO_BACK_BUTTON = {'name': 'Go back', 'url': 'back-link'}


def page_not_found(request, exception):
    if isinstance(exception, dict):
        context = {
            'msg': exception['msg'],
            'link': exception['link'],
            'link_text': exception['link_text'],
        }
    else:
        context = {
            'msg': str(exception),
        }
    extra_context = {
        'back_button': True,
        'role': get_role_of_user(request.user)
    }
    return render(request, 'errors/404.html', context=combine_context(context, extra_context))


def server_error(request):
    return HttpResponseServerError('<h1> 500 Server Error :( </h1>')


def forbidden_error(request, exception):
    context = {
        'msg': str(exception),
        'back_button': True,
        'role': get_role_of_user(request.user)
    }
    return render(request, 'errors/403.html', context=context)
