from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Employee


# Register your models here.
class EmployeeAdmin(MPTTModelAdmin):
    mptt_indent_field = "full_name"
    mptt_level_indent = 20
    list_display = ('full_name', 'emp_position', 'chief', 'date_of_recruit', 'salary', 'id', 'photo_src')
    list_display_links = ('full_name', 'chief')


admin.site.register(Employee, EmployeeAdmin)
