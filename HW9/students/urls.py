from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='students-home'),  # http://127.0.0.1:8000/students/
    path('generate_students/', generate_students, name='gen'),
]
