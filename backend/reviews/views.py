from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer


@api_view(['GET', 'POST'])
def reviews(request, property_id):
    if request.method == 'GET':
        revs = Review.objects.filter(property_id=property_id).select_related('user')
        return Response(ReviewSerializer(revs, many=True).data)

    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()
    data['property'] = property_id
    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_review(request, pk):
    try:
        review = Review.objects.get(pk=pk, user=request.user)
        review.delete()
        return Response({'message': 'Review deleted.'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
