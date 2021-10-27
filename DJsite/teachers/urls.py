from django.urls import path

from teachers.views import TeacherGenerator, GetAllTeachers, GetTeachers, EditTeacher, DeleteTeacher, TeacherProfile

urlpatterns = [
    path('gen-teachers/', TeacherGenerator.as_view(), name='gen-teachers'),
    path('get-all-teachers/', GetAllTeachers.as_view(), name='get-all-teachers'),
    path('search-teachers/', GetTeachers.as_view(), name='search-teachers'),
    path('edit-teacher/<int:pk>', EditTeacher.as_view(), name='edit-teacher'),
    path('delete-teacher/<int:pk>', DeleteTeacher.as_view(), name='delete-teacher'),
    path('teacher-profile/<int:pk>/', TeacherProfile.as_view(), name='teacher-profile'),
]
