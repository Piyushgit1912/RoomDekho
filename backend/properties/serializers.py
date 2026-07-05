# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import Property, PropertyImage,PropertyVideo


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'uploaded_at']

