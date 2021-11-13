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

MENU_FOR_LOGGED_USER = [
    {'name': 'Main Page', 'url': 'users-home', 'id': 1},
    {'name': 'About', 'url': 'about', 'id': 2},
    {'name': 'Links', 'url': 'links', 'id': 3},
    {'name': 'Logout', 'url': 'logout', 'id': 7},
    # {'name': 'Hillel LMS', 'url': 'https://lms.ithillel.ua/', 'id': 6}
]
MENU_FOR_UNLOGGED_USER = [
    {'name': 'Main Page', 'url': 'users-home', 'id': 1},
    {'name': 'About', 'url': 'about', 'id': 2},
    {'name': 'Sign In', 'url': 'login', 'id': 4},
    {'name': 'Register', 'url': 'register', 'id': 5},
    # {'name': 'Hillel LMS', 'url': 'https://lms.ithillel.ua/', 'id': 6}
]

HOME_PAGE_POSTS = [
    {
        'name': '/gen-students/',
        'description': '[admin only] Generates students with opt.param. ?count= (def=10) | Pass: 123faker123',
        'url_name': 'gen-students',
        'permission': 'Staff'
    },
    {
        'name': '/gen-teachers/',
        'description': '[admin only] Generates teachers with opt.param. ?count= (def=10) | Pass: 123faker123',
        'url_name': 'gen-teachers',
        'permission': 'Staff'
    },
    {
        'name': '/get-all-teachers/',
        'description': 'Returns a list of all teachers from DB. You can edit or delete any of them!',
        'url_name': 'get-all-teachers',
        'permission': None
    },
    {
        'name': '/get-all-students/',
        'description': 'Returns a list of all students from DB. You can edit or delete any of them!',
        'url_name': 'get-all-students',
        'permission': None
    },
    {
        'name': '/search-teachers/',
        'description': 'Makes search in Teachers table, per each named column. You can edit every of these.',
        'url_name': 'search-teachers',
        'permission': None
    },
    {
        'name': '/search-students/',
        'description': 'Makes search in Student table per all text type columns via Ajax technology. '
                       'You can edit every of these.',
        'url_name': 'search-students',
        'permission': None
    },
    {
        'name': '/create-user/',
        'description': '[admin only]    Creating a new user using Django Forms',
        'url_name': 'create-user',
        'permission': 'Staff'
    },
]

TEACHER_QUERY_FIELDS = ('first_name',
                        'last_name',
                        'city',
                        'faculty',
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

NO_PROFILE_ANCHOR_PAGE_TITLES = ['Student Profile', 'Teacher Profile']

STUDENT_REQUIRED_FOR_FILLING_FIELDS = ('city', 'birthday', 'phone_number', 'faculty',
                                       'previous_educational_institution', 'course')

TEACHER_REQUIRED_FOR_FILLING_FIELDS = ('city', 'birthday', 'phone_number', 'faculty',
                                       'date_of_employment', 'experience_in_years', 'courses')

TEACHER_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE = ('City',
                                                'Birthday',
                                                'Faculty',
                                                'Date of employment',
                                                'Experience in years')
STUDENT_PROFILE_COLUMN_NAMES_FOR_SEARCH_PAGE = ('City',
                                                'Birthday',
                                                'Faculty',
                                                'Previous educational institution',
                                                'Course')
USER_COLUMN_NAMES_FOR_SEARCH_PAGE = ('First Name', 'Last Name')
