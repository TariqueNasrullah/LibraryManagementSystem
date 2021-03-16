from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    """
    Custom User Configuration for the Django default admin panel.
    """
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Register CustomUser to the Django Admin Panel
admin.site.register(CustomUser, UserAdminConfig)
