from django.http import HttpResponseServerError
from django.shortcuts import render


def page_not_found(request, exception):
    if isinstance(exception, dict):
        context = {
            'msg': exception['msg'],
            'link': exception['link'],
            'link_text': exception['link_text']
        }
    else:
        context = {
            'msg': str(exception),
        }
    return render(request, 'errors/404.html', context=context)


def server_error(request):
    return HttpResponseServerError('<h1> 500 Server Error :( </h1>')


def forbidden_error(request, exception):
    context = {
        'msg': str(exception)
    }
    return render(request, 'errors/403.html', context=context)
