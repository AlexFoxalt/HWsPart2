from marshmallow import fields

student_filter_query = {
    'text': fields.Str(required=False, missing=None)
}

position_and_course_filter_query = {
    'pos': fields.Str(required=False, missing=None),
    'course': fields.Str(required=False, missing=None)
}

options = ['Teacher\'s date of employment',
           'Student\'s previous educational institution',
           'Teacher\'s experience in years',
           'Student\'s course',
           'Teacher\'s courses']

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

positions_selector = [
    (0, 'Student'),
    (1, 'Teacher')
]

faculties_selector = [(fac, fac) for fac in FACULTIES]
