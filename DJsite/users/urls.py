from django.urls import path

from .views import Home, CreateUser, EditUser, GetUsersByCourse

urlpatterns = [
    path('', Home.as_view(), name='users-home'),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('edit-user/<int:pk>', EditUser.as_view(), name='edit-user'),
    path('get-users-by-course/', GetUsersByCourse.as_view(), name='get-users-by-course'),
]
