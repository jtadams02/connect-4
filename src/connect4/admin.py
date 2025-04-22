from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.action(description='Mark selected users as staff')
def make_users_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)

@admin.action(description='Remove staff status from selected users')
def remove_users_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)

class CustomUserAdmin(BaseUserAdmin):
    actions = [make_users_staff, remove_users_staff]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)