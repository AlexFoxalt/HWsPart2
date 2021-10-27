from django.http import HttpResponseServerError
from django.shortcuts import render


def page_not_found(request, exception):
    context = {
        'msg': str(exception)
    }
    return render(request, '404.html', context=context)


def server_error(request):
    return HttpResponseServerError('<h1> 500 Server Error :( </h1>')
