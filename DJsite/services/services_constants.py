"""Here we collect all of constants that we used in project"""
from faker import Faker
from marshmallow import fields
from webargs import djangoparser

parser = djangoparser.DjangoParser()

FAKER = Faker('EN')

INVALID_DOMAIN_NAMES = ('@abc.com',
                        '@123.com',
                        '@xyz.com')

POSSIBLE_EXTENSIONS_FOR_PROFILE = ('txt',
                                   'pdf',
                                   'docx')

KEYS_TO_POP_FOR_TEACHER = ['teacher_courses',
                           'previous_educational_institution',
                           'course',
                           'invited_by']

KEYS_TO_POP_FOR_STUDENT = ['date_of_employment',
                           'experience_in_years',
                           'teacher_courses',
                           'invited_by']

STUDENT_FILTER_QUERY = {
    'text': fields.Str(required=False, missing=None)
}

POSITION_AND_COURSE_FILTER_QUERY = {
    'pos': fields.Str(required=False, missing=None),
    'course': fields.Str(required=False, missing=None)
}

OPTIONS = ['Teacher\'s date of employment',
           'Student\'s previous educational institution',
           'Teacher\'s experience in years',
           'Student\'s course',
           'Teacher\'s courses',
           'Student\'s resume',
           'Student\'s email invited by']

MENU = [
    {'name': 'Main Page', 'url': 'users-home', 'id': 1},
    {'name': 'About', 'url': 'users-home', 'id': 2},
    {'name': 'Links', 'url': 'users-home', 'id': 3},
    {'name': 'Hillel LMS', 'url': 'https://lms.ithillel.ua/', 'id': 4}
]

HOME_PAGE_POSTS = [
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
        'description': 'Makes search in Teachers table, per each named column. You can edit every of these.',
        'url_name': 'search-teachers'
    },
    {
        'name': '/search-students/',
        'description': 'Makes search in Student table per all text type columns via Ajax technology. '
                       'You can edit every of these.',
        'url_name': 'search-students'
    },
    {
        'name': '/create-user/',
        'description': 'Creating a new user using Django Forms',
        'url_name': 'create-user'
    },
]

TEACHER_QUERY_FIELDS = ('first_name',
                        'last_name',
                        'city',
                        'email',
                        'faculty',
                        'phone_number',
                        'position',
                        'birthday',
                        'date_of_employment',
                        'experience_in_years')

TEACHER_FILTER_QUERY = {
    key: fields.Str(required=False, missing=None) for key in TEACHER_QUERY_FIELDS
}

GET_INT_COUNT = {
    "count": fields.Int(
        required=False,
        missing=10
    )
}

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

POSITIONS_SELECTOR = [
    ('Student', 'Student'),
    ('Teacher', 'Teacher')
]

FACULTIES_SELECTOR = [(fac, fac) for fac in FACULTIES]
