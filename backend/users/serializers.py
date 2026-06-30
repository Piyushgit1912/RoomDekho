# pyrefly: ignore [missing-import]
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Favorite


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
