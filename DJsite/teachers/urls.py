from django.urls import path

from teachers.views import TeacherGenerator, GetAllTeachers, GetTeachers, EditTeacher, TeacherProfile, \
    TeacherContinuedRegistration

urlpatterns = [
    path('gen-teachers/', TeacherGenerator.as_view(), name='gen-teachers'),
    path('get-all-teachers/', GetAllTeachers.as_view(), name='get-all-teachers'),
    path('search-teachers/', GetTeachers.as_view(), name='search-teachers'),
    path('edit-teacher/<int:pk>', EditTeacher.as_view(), name='edit-teacher'),
    path('teacher-profile/<int:pk>/', TeacherProfile.as_view(), name='teacher-profile'),
    path('register/next-step/<int:pk>/teacher/',
         TeacherContinuedRegistration.as_view(),
         name='register-next-step-teacher')
]
