from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='users-home'),
    path('gen-students/', generate_students),
    path('gen-teachers/', generate_teachers),
    path('get-all-teachers/', get_all_teachers),
    path('get-all-students/', get_all_students),
    path('teachers/', get_teachers),
    path('students/', get_students)
]
