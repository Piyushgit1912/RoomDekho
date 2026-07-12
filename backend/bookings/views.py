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
