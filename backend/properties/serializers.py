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
