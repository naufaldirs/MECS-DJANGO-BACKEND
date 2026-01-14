from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Department, User, Employee, Operator

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('nip', 'full_name', 'department')
    search_fields = ('nip', 'full_name')
    list_filter = ('department',)

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('employee', 'group')
    list_filter = ('group',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Employee Info', {'fields': ('employee',)}),
    )