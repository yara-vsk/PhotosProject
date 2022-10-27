import re
from io import BytesIO
from rest_framework import serializers
from .models import Photo
import requests
from PIL import Image


def save_png(url):
    try:
        with Image.open(BytesIO(requests.get(url).content)) as png_f:
            png_f_heigth = png_f.height
            png_f_width = png_f.width
            color = re.search(r'/[0-9a-fA-F]{3,6}.png$', url)
            png_f_dominate_color = url[color.start() + 1:-4]
            url_local = 'media/' + str(png_f_width) + 'x' + str(png_f_heigth) + '_' + png_f_dominate_color + '.png'
            png_f.save(url_local, format='png')
        if int(png_f_heigth) and int(png_f_width) and png_f_dominate_color:
            return (png_f_heigth, png_f_width, png_f_dominate_color)
        return False
    except:
        return False


class PhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    albumId = serializers.IntegerField()
    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)
    dominant_color = serializers.CharField(max_length=6, read_only=True)
    url_ext = serializers.CharField(max_length=255, write_only=True)
    url = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        url = validated_data['url_ext'] + '.png'
        photo_data = save_png(url)
        if photo_data:
            return Photo.objects.create(
                title=validated_data['title'],
                albumId=validated_data['albumId'],
                width=photo_data[1],
                height=photo_data[0],
                dominant_color=photo_data[2]
            )
        raise serializers.ValidationError("Url is not correct")

    def update(self, instance, validated_data):
        url = validated_data['url_ext'] + '.png'
        photo_data = save_png(url)
        if photo_data:
            validated_data['width']=photo_data[1]
            validated_data['height'] = photo_data[0]
            validated_data['dominant_color'] = photo_data[2]
            instance.title = validated_data.get('title', instance.title)
            instance.albumId = validated_data.get('albumId', instance.albumId)
            instance.width =validated_data.get('width', instance.width)
            instance.height = validated_data.get('height', instance.height)
            instance.dominant_color = validated_data.get('dominant_color', instance.dominant_color)
            instance.save()
            return instance
        raise serializers.ValidationError("Url is not correct")


class PhotoImportSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    albumId = serializers.IntegerField()
    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)
    dominant_color = serializers.CharField(max_length=6, read_only=True)
    url = serializers.CharField(max_length=255,write_only=True)

    def create(self, validated_data):
        url = validated_data['url'] + '.png'
        #print(url)
        photo_data = save_png(url)
        if photo_data:
            return Photo.objects.create(
                title=validated_data['title'],
                albumId=validated_data['albumId'],
                width=photo_data[1],
                height=photo_data[0],
                dominant_color=photo_data[2]
            )
        raise serializers.ValidationError("Url is not correct")