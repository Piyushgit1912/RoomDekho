from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Favorite


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
