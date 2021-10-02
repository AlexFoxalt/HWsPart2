from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='teachers-home'),  # http://127.0.0.1:8000/teachers/
]
