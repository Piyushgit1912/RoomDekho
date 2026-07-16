from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer


@api_view(['GET', 'POST'])
def reviews(request, property_id):
