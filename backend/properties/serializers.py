# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import Property, PropertyImage,PropertyVideo


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'uploaded_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class PropertyVideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyVideo
        fields = ['id', 'video', 'video_url']

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video and request:
            return request.build_absolute_uri(obj.video.url)
        return None

class PropertyListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'price', 'location', 'city', 'room_type',
            'furnished_status', 'gender_preference', 'status',
            'wifi', 'parking', 'ac', 'food', 'security',
            'owner_name', 'primary_image', 'image_count', 'avg_rating', 'review_count',
            'latitude', 'longitude',
            'is_available', 'created_at',
        ]

    def get_primary_image(self, obj):
        request = self.context.get('request')
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        if img and img.image and request:
            return request.build_absolute_uri(img.image.url)
        return None

    def get_image_count(self, obj):
        return obj.images.count()


class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ['owner', 'status', 'is_available', 'created_at', 'updated_at']
