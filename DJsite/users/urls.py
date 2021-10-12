from django.urls import path

from .views import StudentHome, StudentGenerator, TeacherGenerator, GetAllTeachers, GetAllStudents, GetTeachers, \
    GetStudents, CreateUser, CreateTeacher, CreateStudent, EditStudent, DeleteStudent, EditUser, EditTeacher, \
    DeleteTeacher

urlpatterns = [
    path('', StudentHome.as_view(), name='users-home'),
    path('gen-students/', StudentGenerator.as_view(), name='gen-students'),
    path('gen-teachers/', TeacherGenerator.as_view(), name='gen-teachers'),
    path('get-all-teachers/', GetAllTeachers.as_view(), name='get-all-teachers'),
    path('get-all-students/', GetAllStudents.as_view(), name='get-all-students'),
    path('teachers/', GetTeachers.as_view(), name='teachers'),
    path('students/', GetStudents.as_view(), name='students'),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('create-teacher/', CreateTeacher.as_view(), name='create-teacher'),
    path('create-student/', CreateStudent.as_view(), name='create-student'),
    path('edit-user/<int:pk>', EditUser.as_view(), name='edit-user'),
    path('edit-student/<int:pk>', EditStudent.as_view(), name='edit-student'),
    path('edit-teacher/<int:pk>', EditTeacher.as_view(), name='edit-teacher'),
    path('delete-student/<int:pk>', DeleteStudent.as_view(), name='delete-student'),
    path('delete-teacher/<int:pk>', DeleteTeacher.as_view(), name='delete-teacher')
]
