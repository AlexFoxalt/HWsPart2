from django.urls import path

from students.views import StudentGenerator, GetAllStudents, GetStudents, EditStudent, DeleteStudent, StudentProfile, \
    StudentContinuedRegistration

urlpatterns = [
    path('gen-students/', StudentGenerator.as_view(), name='gen-students'),
    path('get-all-students/', GetAllStudents.as_view(), name='get-all-students'),
    path('search-students/', GetStudents.as_view(), name='search-students'),
    path('edit-student/<int:pk>', EditStudent.as_view(), name='edit-student'),
    path('delete-student/<int:pk>', DeleteStudent.as_view(), name='delete-student'),
    path('student-profile/<int:pk>/', StudentProfile.as_view(), name='student-profile'),
    path('register/next-step/<int:pk>/student/',
         StudentContinuedRegistration.as_view(),
         name='register-next-step-student')
]
