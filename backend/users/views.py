from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser, Favorite
from .serializers import (UserRegisterSerializer, UserLoginSerializer,
                          UserProfileSerializer, FavoriteSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
            'message': 'Registration successful!'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
            'message': 'Login successful!'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'message': 'Logged out successfully.'})


@api_view(['GET', 'PUT', 'PATCH'])
def profile(request):
    user = request.user
    if request.method == 'GET':
        return Response(UserProfileSerializer(user).data)
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def favorites(request):
    if request.method == 'GET':
        favs = Favorite.objects.filter(user=request.user).select_related('property')
        serializer = FavoriteSerializer(favs, many=True, context={'request': request})
        return Response(serializer.data)

    property_id = request.data.get('property_id')
    if not property_id:
        return Response({'error': 'property_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    fav, created = Favorite.objects.get_or_create(
        user=request.user, property_id=property_id)
    if not created:
        fav.delete()
        return Response({'message': 'Removed from favorites.', 'favorited': False})
    return Response({'message': 'Added to favorites.', 'favorited': True},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def admin_delete_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response({'message': 'User deleted.'})
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
