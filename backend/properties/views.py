from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Property, PropertyImage,PropertyVideo
from .serializers import (PropertyListSerializer, PropertyDetailSerializer,
                           PropertyCreateSerializer, PropertyImageSerializer)


class PropertyListView(generics.ListAPIView):
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Property.objects.filter(
            status='approved', is_available=True
        ).prefetch_related('images', 'reviews')

        p = self.request.query_params
