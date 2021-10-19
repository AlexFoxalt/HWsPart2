from random import choice

import django
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from faker import Faker
from marshmallow import fields
from webargs import djangoparser

parser = djangoparser.DjangoParser()
f = Faker('EN')

MENU = [
    {'name': 'Main Page', 'url': 'users-home', 'id': 1},
    {'name': 'About', 'url': 'users-home', 'id': 2},
    {'name': 'Links', 'url': 'users-home', 'id': 3},
    {'name': 'Hillel LMS', 'url': 'https://lms.ithillel.ua/', 'id': 4}
]

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
        'description': 'Returns a list of all teachers from DB. You can edit or delete any of them!',
        'url_name': 'get-all-teachers'
    },
    {
        'name': '/get-all-students/',
        'description': 'Returns a list of all students from DB. You can edit or delete any of them!',
        'url_name': 'get-all-students'
    },
    {
        'name': '/search-teachers/',
        'description': 'Makes search in Teachers table, per each named column ',
        'url_name': 'search-teachers'
    },
    {
        'name': '/search-students/',
        'description': 'Makes search in Student table per all text type columns via Ajax technology',
        'url_name': 'search-students'
    },
    {
        'name': '/create-user/',
        'description': 'Creating a new user using Django Forms',
        'url_name': 'create-user'
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
    (0, 'Student'),
    (1, 'Teacher')
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
options = ['Date of employment',
           'Previous educational institution',
           'Experience in years']
CONTEXT_CONTAINER = {
    1: {'title': 'Main Page', 'selected': 1, 'posts': home_page_posts,
        'possible_positions': positions_selector, 'faculties': FACULTIES},
    2: {'title': 'All teachers', 'user_class': 'Teacher(s)'},
    3: {'title': 'All students', 'user_class': 'Student(s)'},
    4: {'title': 'Create User', 'url': 'create-user', 'options': options},
    5: {'title': 'Edit Student', 'position': 'Student', 'url': 'delete-student'},
    6: {'title': 'Edit Teacher', 'position': 'Teacher', 'url': 'delete-teacher'},
    7: {'title': 'Delete Student', 'position': 'Student'},
    8: {'title': 'Delete Teacher', 'position': 'Teacher'},
    9: {'title': 'Create Teacher', 'url': 'create-teacher'}
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
            'posts': posts,
            'menu': MENU
        }
        return render(request, cls.template_name, context=context)


class EntitySearchMixinBase:
    model = None
    template_name = 'search_of_users.html'
    context_object_name = 'content'

    @classmethod
    def get_context_data(cls):
        posts = cls.model.objects.all()
        class_name = cls.model.__name__

        context = {
            'title': f'{class_name}s searching',
            'user_class': f'{class_name}(s)',
            'posts': posts,
            'menu': MENU,
        }
        return context


class EntitySearchPerOneFieldMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, *args, **kwargs):
        context = super().get_context_data()
        applied_filters = []
        searching_keys = args[0]

        for key, value in searching_keys.items():
            if value is not None and value:
                context['posts'] = context['posts'].filter(**{f'{key}__contains': value})
                applied_filters.append(f'{key} --- {value}')

        context['applied_filters'] = applied_filters
        context['searching_fields'] = from_dict_to_list_of_dicts_format(searching_keys)
        return render(request, 'search_of_users.html', context=context)


class EntitySearchPerAllFieldsMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, text, *args, **kwargs):
        context = super().get_context_data()
        ajax_filter = request.GET.get('text', None)

        searching_keys = ajax_filter if ajax_filter is not None else text['text']

        if searching_keys is not None:
            text_fields = [f.name for f in cls.model._meta.get_fields() if
                           isinstance(f, django.db.models.fields.CharField)]
            or_cond = Q()

            for field in text_fields:
                or_cond |= Q(**{'{}__contains'.format(field): searching_keys})

            context['posts'] = context['posts'].filter(or_cond)

        context['searching_fields'] = from_dict_to_list_of_dicts_format(text)

        if request.is_ajax():
            html = render_to_string(
                template_name="posts-results-partial.html",
                context=context
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'search_of_users.html', context=context)


class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = MENU
        context['selected'] = 0
        page_id = kwargs['page_id']

        container = CONTEXT_CONTAINER.get(page_id, None)
        context.update(container)
        return context


def mine_faker_of_faculties():
    return choice(FACULTIES)


def combine_context(cont1, cont2):
    return dict(**cont1, **cont2)


def from_dict_to_list_of_dicts_format(arg: dict):
    return list({'field': field, 'value': value} for field, value in arg.items())


class GetAllUsersMixin(ContextMixin, ListView):
    def get(self, request, *args, **kwargs):
        posts = self.model.objects.all()
        columns = [f.get_attname() for f in self.model._meta.fields]
        context = self.get_user_context(page_id=self.page_id,
                                        posts=posts,
                                        columns=columns)
        return render(request, self.template_name, context=context)
