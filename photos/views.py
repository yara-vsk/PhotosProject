from django.shortcuts import render
from .models import Photo
from .serializers import PhotoSerializer, PhotoImportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
import requests


class PhotoAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            try:
                photos = Photo.objects.annotate(
                    url=Concat(V('/media/'), 'width', V('x'), 'height', V('_'), 'dominant_color', V('.png'),
                               output_field=CharField())).values('id', 'title', 'albumId',
                                                                 'width', 'height',
                                                                 'dominant_color', 'url')
                serializer = PhotoSerializer(photos, many=True)
                return Response(serializer.data)
            except:
                return Response({'error': "There are no objects in database"})
        try:
            photos = Photo.objects.filter(pk=pk).annotate(
                url=Concat(V('/media/'), 'width', V('x'), 'height', V('_'), 'dominant_color', V('.png'),
                           output_field=CharField())).values('id', 'title', 'albumId', 'width', 'height',
                                                             'dominant_color', 'url')


            serializer = PhotoSerializer(photos[0])
            return Response(serializer.data)
        except:
            return Response({'error':"Object does not exists"})

    def post(self, request):
        data = request.data
        data['url_ext']=data['url']
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error':"Method PUT not allowed"})
        try:
            instance=Photo.objects.get(pk=pk)
        except:
            return Response({'error':"Object does not exists"})
        data = request.data
        data['url_ext'] = data['url']
        serializer=PhotoSerializer(data=data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error':"Method DELETE not allowed"})
        try:
            instance=Photo.objects.get(pk=pk).delete()
            return Response({'post': "delete photo - id "+str(pk)})
        except:
            return Response({'error':"Object does not exists"})


class PhotoImportView(APIView):
    def get(self, request):
        pfotos_list=requests.get('https://jsonplaceholder.typicode.com/photos').json()
        serializer = PhotoImportSerializer(data=pfotos_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PhotoImportSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







