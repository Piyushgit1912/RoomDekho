from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser, Favorite
from .serializers import (UserRegisterSerializer, UserLoginSerializer,
                          UserProfileSerializer, FavoriteSerializer)


