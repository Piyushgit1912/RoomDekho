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

        if p.get('search'):
            qs = qs.filter(
                Q(title__icontains=p['search']) |
                Q(city__icontains=p['search']) |
                Q(location__icontains=p['search'])
            )
        if p.get('city'):
            qs = qs.filter(city__icontains=p['city'])
        if p.get('room_type'):
            qs = qs.filter(room_type=p['room_type'])
        if p.get('furnished_status'):
            qs = qs.filter(furnished_status=p['furnished_status'])
        if p.get('gender_preference'):
            qs = qs.filter(gender_preference=p['gender_preference'])
        if p.get('min_price'):
            qs = qs.filter(price__gte=p['min_price'])
        if p.get('max_price'):
            qs = qs.filter(price__lte=p['max_price'])

        for amenity in ['wifi', 'parking', 'ac', 'food', 'gym', 'security']:
            if p.get(amenity) == 'true':
                qs = qs.filter(**{amenity: True})

        ordering = p.get('ordering', '-created_at')
        allowed_orderings = ['price', '-price', '-created_at', 'created_at']
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
