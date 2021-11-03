from django.urls import path
from django.contrib.auth import views as auth_views

from .password_reset_views import UsersPasswordResetView, UsersPasswordResetDoneView, UsersPasswordResetConfirmView, \
    UsersPasswordResetCompleteView
from .tests import TestResetFormEmail
from .views import Home, CreateUser, EditUser, GetUsersByCourse, RegisterUser, LoginUser, About, Links, \
    LogoutUser, UserContinuedRegistration, UserProfile

urlpatterns = [
    path('', Home.as_view(), name='users-home'),
    path('about/', About.as_view(), name='about'),
    path('links/', Links.as_view(), name='links'),

    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('edit-user/<int:pk>', EditUser.as_view(), name='edit-user'),
    path('get-users-by-course/', GetUsersByCourse.as_view(), name='get-users-by-course'),
    path('user-profile/<str:username>', UserProfile.as_view(), name='user-profile'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('register/next-step/<int:pk>/', UserContinuedRegistration.as_view(), name='register-next-step'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

    path('reset-password/', UsersPasswordResetView.as_view(), name='reset_password'),
    path('reset-password-sent/', UsersPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UsersPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', UsersPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
