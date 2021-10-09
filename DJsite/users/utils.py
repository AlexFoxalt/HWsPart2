from random import choice
from django.db.models import Q
from django.shortcuts import render
from faker import Faker
from marshmallow import fields
from webargs import djangoparser

parser = djangoparser.DjangoParser()
f = Faker('EN')

home_page_posts = [
    {
        'name': '/gen-students/',
        'description': 'Generates students with opt.param. ?count= (def=10)',
        'url_name': 'gen-students'
    },
    {
        'name': '/gen-teachers/',
        'description': 'Generates teachers with opt.param. ?count= (def=10)',
        'url_name': 'gen-teachers'
    },
    {
        'name': '/get-all-teachers/',
        'description': 'Returns a list of all teachers from DB',
        'url_name': 'get-all-teachers'
    },
    {
        'name': '/get-all-students/',
        'description': 'Returns a list of all students from DB',
        'url_name': 'get-all-students'
    },
    {
        'name': '/teachers/',
        'description': 'Makes search in Teachers table, per each named column '
                       '| possible params: ?name=, ?city=, ?email=, ?faculty=, ?date_of_employment=,'
                       ' ?experience_in_years=',
        'url_name': 'teachers'
    },
    {
        'name': '/students/',
        'description': 'Makes search in Student table per all text type columns '
                       '| possible param: ?text=',
        'url_name': 'students'
    },
    {
        'name': '/create-user/',
        'description': 'Creating a new user using Django Forms',
        'url_name': 'create-user'
    },
    {
        'name': '/create-teacher/',
        'description': 'Creating a new teacher using Django Forms',
        'url_name': 'create-teacher'
    },
    {
        'name': '/create-student/',
        'description': 'Creating a new student using Django Forms',
        'url_name': 'create-student'
    },
]

FACULTIES = [
    'Accounting and Finance',
    'Aeronautical and Manufacturing',
    'Engineering',
    'Agriculture and Forestry',
    'Anatomy and Physiology',
    'Anthropology',
    'Archaeology',
    'Architecture',
    'Art and Design',
    'Biological',
    'Sciences',
    'Building',
    'Business and Management',
    'Studies',
    'Chemical',
    'Engineering',
    'Chemistry',
    'Civil',
    'Engineering',
    'Classics and Ancient',
    'History',
    'Communication and Media',
    'Studies',
    'Complementary',
    'Medicine',
    'Computer',
    'Science',
    'Counselling',
    'Creative',
    'Writing',
    'Criminology',
    'Dentistry',
    'Drama',
    'Dance and Cinematics',
    'Economics',
    'Education',
    'Electrical and Electronic',
    'Engineering',
    'English',
    'Fashion',
    'Film Making',
    'Food',
    'Science',
    'Forensic',
    'Science',
    'General',
    'Engineering',
    'Geography and Environmental',
    'Sciences',
    'Geology',
    'Health And Social',
    'Care',
    'History',
    'History of Art',
    'Architecture and Design',
    'Hospitality',
    'Leisure',
    'Recreation and Tourism',
    'Information',
    'Technology',
    'Land and Property',
    'Management',
    'Law',
    'Linguistics',
    'Marketing',
    'Materials',
    'Technology',
    'Mathematics',
    'Mechanical',
    'Engineering',
    'Medical',
    'Technology',
    'Medicine',
    'Music',
    'Nursing',
    'Occupational',
    'Therapy',
    'Pharmacology and Pharmacy',
    'Philosophy',
    'Physics and Astronomy',
    'Physiotherapy',
    'Politics',
    'Psychology',
    'Robotics',
    'Social',
    'Policy',
    'Social',
    'Work',
    'Sociology',
    'Sports',
    'Science',
    'Veterinary',
    'Medicine',
    'Youth',
    'Work',
]

faculties_selector = [(fac, fac) for fac in FACULTIES]

positions_selector = [
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
]

teacher_query_fields = ('first_name',
                        'last_name',
                        'city',
                        'email',
                        'faculty',
                        'phone_number',
                        'position',
                        'birthday',
                        'date_of_employment',
                        'experience_in_years')

teacher_filter_query = {
    key: fields.Str(required=False, missing=None) for key in teacher_query_fields
}

get_int_count = {
    "count": fields.Int(
        required=False,
        missing=10
    )
}

student_filter_query = {
    'text': fields.Str(required=False, missing=None)
}


class EntityGeneratorMixin:
    model = None
    template_name = 'entity_generator.html'
    context_object_name = 'content'

    @classmethod
    def get(cls, request, count, user_class, *args, **kwargs):
        cls.model.generate_entity(count)

        posts = cls.model.objects.all().order_by('-id')[:count][::-1]

        context = {
            'title': f'{user_class} generator',
            'user_class': user_class,
            'posts': posts
        }
        return render(request, cls.template_name, context=context)


class EntitySearchMixinBase:
    model = None
    template_name = 'search_of_users.html'
    context_object_name = 'content'


class EntitySearchPerOneFieldMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, user_class, *args, **kwargs):
        posts = cls.model.objects.all()
        applied_filters = []
        searching_keys = args[0]

        for key, value in searching_keys.items():
            if value is not None:
                posts = posts.filter(**{f'{key}__contains': value})
                applied_filters.append(f'{key} ~ "{value}"')

        context = {
            'title': f'{user_class} searching',
            'user_class': user_class,
            'applied_filters': applied_filters,
            'posts': posts
        }
        return render(request, 'search_of_users.html', context=context)


class EntitySearchPerAllFieldsMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, user_class, text, *args, **kwargs):
        posts = cls.model.objects.all()
        search_filter = text['text']

        if search_filter is not None:
            fields_of_search = ['name', 'city', 'email', 'faculty', 'previous_educational_institution']
            or_cond = Q()

            for field in fields_of_search:
                or_cond |= Q(**{'{}__contains'.format(field): search_filter})

            posts = posts.filter(or_cond)

        context = {
            'title': f'{user_class} searching',
            'user_class': user_class,
            'applied_filters': text.values(),
            'posts': posts
        }
        return render(request, 'search_of_users.html', context=context)


def mine_faker_of_faculties():
    return choice(FACULTIES)
