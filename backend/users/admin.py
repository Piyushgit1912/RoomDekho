from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Favorite


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'name', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'name', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('name', 'phone', 'user_type', 'profile_image')}),
    )
