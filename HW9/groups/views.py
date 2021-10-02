from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('Group App start-screen')
