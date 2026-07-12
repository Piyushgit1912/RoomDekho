from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_inquiry(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Inquiry sent!', 'booking': serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_inquiries(request):
    bookings = Booking.objects.filter(user=request.user).select_related('property')
    return Response(BookingSerializer(bookings, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def owner_inquiries(request):
    bookings = Booking.objects.filter(
        property__owner=request.user).select_related('property', 'user')
    return Response(BookingSerializer(bookings, many=True).data)
