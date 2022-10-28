
from rest_framework import serializers
from .models import Photo



class PhotoSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    albumId = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    dominant_color = serializers.CharField(max_length=6)
    url = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.albumId = validated_data.get('albumId', instance.albumId)
        instance.width =validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.dominant_color = validated_data.get('dominant_color', instance.dominant_color)
        instance.save()
        return instance

