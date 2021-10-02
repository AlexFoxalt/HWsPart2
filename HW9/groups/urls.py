from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='groups-home'),  # http://127.0.0.1:8000/groups/
]
