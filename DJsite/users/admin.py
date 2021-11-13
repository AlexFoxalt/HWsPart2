from django.contrib import admin

from .models import Person, Course, CustomUser


# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'birthday', 'phone_number', 'faculty', 'position', 'filled')
    list_display_links = ('user', )
    search_fields = ('city', 'faculty')
    list_editable = ('filled',)
    list_filter = ('birthday', 'filled')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_display_links = ('email', 'nickname')
    search_fields = ('email', 'nickname', 'first_name', 'last_name')
    list_editable = ('is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')


admin.site.register(Person, PersonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
