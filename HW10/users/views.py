from django.http import HttpResponse, HttpResponseBadRequest
from .utils import teacher_filter_query, student_filter_query
from .models import Student, Teacher
from webargs.djangoparser import use_kwargs
from django.db.models import Q


# Create your views here.


def index(request):
    return HttpResponse('<h1> Possible urls </h1>'
                        '<ul>'
                        '<li>/gen-students/ ===== Generates students with opt.param. *count* (def=10)</li>'
                        '<li>/gen-teachers/ ===== Generates teachers with opt.param. *count* (def=10)</li>'
                        '<li>/get-all-teachers/ === Returns a list of all teachers from DB</li>'
                        '<li>/get-all-students/ === Returns a list of all students from DB</li>'
                        '<li>/teachers/ ======== Makes search in Teachers table, per each named column'
                        ' | possible params: name, city, email, faculty, date_of_employment, experience_in_years</li>'
                        '<li>/students/ ======== Makes search in Student table per all text type columns'
                        ' | possible param: text</li>'
                        '</ul>')


def generate_students(request):
    try:
        count = int(request.GET.get('count', 10))
    except ValueError as err:
        return HttpResponseBadRequest(request, err)

    Student.generate_entity(count)

    last_added = map(str, Student.objects.all().order_by('-id')[:count][::-1])
    sep = '<br>'
    return HttpResponse(f'List of students that were added:<br>'
                        f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}')


def generate_teachers(request):
    try:
        count = int(request.GET.get('count', 10))
    except ValueError as err:
        return HttpResponseBadRequest(request, err)

    Teacher.generate_entity(count)

    last_added = map(str, Teacher.objects.all().order_by('-id')[:count][::-1])
    sep = '<br>'
    return HttpResponse(f'List of teachers that were added:<br>'
                        f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}')


def get_all_teachers(request):
    return HttpResponse('<br>'.join(map(str, Teacher.objects.all())))


def get_all_students(request):
    return HttpResponse('<br>'.join(map(str, Student.objects.all())))


@use_kwargs(teacher_filter_query, location='query')
def get_teachers(request, name, city, email, faculty, date_of_employment, experience_in_years):
    data = Teacher.objects.all()

    applied_filters = []

    if name is not None:
        data = data.filter(name__contains=name)
        applied_filters.append(f'name ~ "{name}"')
    if city is not None:
        data = data.filter(city__contains=city)
        applied_filters.append(f'city ~ "{city}"')
    if email is not None:
        data = data.filter(email__contains=email)
        applied_filters.append(f'name ~ "{email}"')
    if faculty is not None:
        data = data.filter(faculty__contains=faculty)
        applied_filters.append(f'faculty ~ "{faculty}"')
    if date_of_employment is not None:
        data = data.filter(date_of_employment__contains=date_of_employment)
        applied_filters.append(f'date_of_employment ~ "{date_of_employment}"')
    if experience_in_years is not None:
        data = data.filter(experience_in_years__contains=experience_in_years)
        applied_filters.append(f'experience_in_years ~ "{experience_in_years}"')

    return HttpResponse(f'Success! <br>'
                        f'Applied filters: <ul><li>'
                        f'{"</li><li>".join(applied_filters) if applied_filters else "No filters"}'
                        f'</li></ul><br>'
                        f'Here is result: <br> {"<br>".join(map(str, data))}')


@use_kwargs(student_filter_query, location='query')
def get_students(request, text):
    res = Student.objects.filter(
        Q(name__contains=text) |
        Q(city__contains=text) |
        Q(email__contains=text) |
        Q(faculty__contains=text) |
        Q(previous_educational_institution__contains=text)
    )
    return HttpResponse(f'Success here\'s result: <br><br>'
                        f'Applied filters: text= {text if text else "No filter"}<br><br>'
                        f'{"<br>".join(map(str, res))}')
