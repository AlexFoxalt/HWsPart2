from django.contrib import admin
from django.db.models import Count

from services.services_functions import get_age_from_birthday
from students.models import Student
from .models import Person, Course, CustomUser


# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'birthday', 'Age', 'phone_number', 'faculty', 'position', 'filled')
    list_display_links = ('user',)
    search_fields = ('city', 'faculty')
    list_editable = ('filled',)
    list_filter = ('birthday', 'filled')

    def Age(self, obj):
        birthday = obj.birthday
        if birthday is None:
            return '---'
        return get_age_from_birthday(birthday)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_students_count', 'view_teachers_count')
    list_display_links = ('name',)

    def view_students_count(self, obj):
        return Student.objects.filter(course_id=obj.pk).count()

    def view_teachers_count(self, obj):
        return obj.teacher_set.all().count()

    view_students_count.short_description = "Students"
    view_teachers_count.short_description = "Teachers"


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_display_links = ('email', 'nickname')
    search_fields = ('email', 'nickname', 'first_name', 'last_name')
    list_editable = ('is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')


admin.site.register(Person, PersonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
