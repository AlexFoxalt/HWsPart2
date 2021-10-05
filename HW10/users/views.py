from django.http import HttpResponse
from .utils import teacher_filter_query, student_filter_query, get_int_count
from .models import Student, Teacher
from webargs.djangoparser import use_kwargs, use_args
from django.db.models import Q
from webargs import djangoparser
from django.core.exceptions import BadRequest

# Create your views here.
parser = djangoparser.DjangoParser()


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


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


@parser.use_kwargs(get_int_count, location="query")
def generate_students(request, count):
    Student.generate_entity(count)

    last_added = map(str, Student.objects.all().order_by('-id')[:count][::-1])
    sep = '<br>'
    return HttpResponse(f'List of students that were added:<br>'
                        f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}')


@parser.use_kwargs(get_int_count, location="query")
def generate_teachers(request, count):
    Teacher.generate_entity(count)

    last_added = map(str, Teacher.objects.all().order_by('-id')[:count][::-1])
    sep = '<br>'
    return HttpResponse(f'List of teachers that were added:<br>'
                        f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}')


def get_all_teachers(request):
    return HttpResponse('<br>'.join(map(str, Teacher.objects.all())))


def get_all_students(request):
    return HttpResponse('<br>'.join(map(str, Student.objects.all())))


@use_args(teacher_filter_query, location='query')
def get_teachers(request, args):
    data = Teacher.objects.all()
    applied_filters = []

    for key, value in args.items():
        if value is not None:
            data = data.filter(**{f'{key}__contains': value})
            applied_filters.append(f'{key} ~ "{value}"')

    return HttpResponse(f'Success! <br>'
                        f'Applied filters: <ul><li>'
                        f'{"</li><li>".join(applied_filters) if applied_filters else "No filters"}'
                        f'</li></ul><br>'
                        f'Here is result: <br> {"<br>".join(map(str, data))}')


@use_kwargs(student_filter_query, location='query')
def get_students(request, text):
    if text is not None:
        fields = ['name', 'city', 'email', 'faculty', 'previous_educational_institution']
        students = Student.objects.all()
        or_cond = Q()

        for field in fields:
            or_cond |= Q(**{'{}__contains'.format(field): text})

        students = students.filter(or_cond)
    else:
        students = students = Student.objects.all()

    return HttpResponse(f'Success here\'s result: <br><br>'
                        f'Applied filters: text= {text if text else "No filter"}<br><br>'
                        f'{"<br>".join(map(str, students))}')
