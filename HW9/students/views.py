from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from faker import Faker
from students.models import Student
from students.webargs_utils import IntParamFromOneToFifty
from marshmallow import ValidationError

fake = Faker()

# Create your views here.


def index(request):
    return HttpResponse(f'<h1> Student-app Home Page <h1>')


def generate_students(request):
    try:
        count = IntParamFromOneToFifty().load(request.GET)["count"]
    except ValidationError as err:
        return BadRequest(request, err)

    for num in range(count):
        StudName = fake.name()
        StudCity = fake.city()
        Student.objects.create(name=StudName, city=StudCity)

    last_added = map(str, Student.objects.all().order_by('-id')[:count][::-1])
    return HttpResponse(f'List of students that were added: <br>'
                        f'{"<br>".join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}')


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1> 404 Page Not Found :( </h1>')


def BadRequest(request, exception):
    return HttpResponseBadRequest('<h1> 400 Bad Request :( </h1>')


def ServerError(request):
    return HttpResponseServerError('<h1> 500 Server Error :( </h1>')
