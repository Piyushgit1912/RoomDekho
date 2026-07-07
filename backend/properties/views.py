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
def property_detail(request, pk):
    try:
        prop = Property.objects.prefetch_related('images', 'reviews').get(pk=pk)
        if prop.status != 'approved':
            is_owner = request.user.is_authenticated and prop.owner == request.user
            is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.user_type == 'admin')
            if not (is_owner or is_admin):
                return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Property.DoesNotExist:
        return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PropertyDetailSerializer(prop, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.IsAuthenticated])
def add_property(request):
    if request.user.user_type not in ['owner', 'admin']:
        return Response(
            {'error': 'Only property owners can add listings.'},
            status=status.HTTP_403_FORBIDDEN)

    serializer = PropertyCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        prop = serializer.save()
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            PropertyImage.objects.create(property=prop, image=image, is_primary=(i == 0))
        
        video=request.FILES.get('video')
        if video:
            PropertyVideo.objects.create(property=prop,video=video)
        return Response({
            'message': 'Property submitted for approval.',
            'property': PropertyDetailSerializer(prop, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_property(request, pk):
    try:
        prop = Property.objects.get(pk=pk, owner=request.user)
    except Property.DoesNotExist:
        return Response({'error': 'Not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PropertyDetailSerializer(prop, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(status='approved')
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_property(request, pk):
    try:
        if request.user.is_staff:
