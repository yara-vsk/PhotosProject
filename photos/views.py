
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
import asyncio
from .datahandler import get_import_fotos_data, get_import_foto_data
from .fotocreator import save_fotos_from_urls, save_png


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

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            return Response({'error': "Method POST not allowed"})
        if isinstance(request.data,list):
            return Response({'error': "POST only 1 object"})
        data = get_import_foto_data(request.data)
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                save_png(request.data.get('url'))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': "Json is not correct"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error':"Method PUT not allowed"})
        try:
            instance=Photo.objects.get(pk=pk)
        except:
            return Response({'error':"Object does not exists"})
        if isinstance(request.data,list):
            return Response({'error': "PUT only 1 object"})
        data = get_import_foto_data(request.data)
        serializer=PhotoSerializer(data=data,instance=instance)
        if serializer.is_valid():
            try:
                serializer.save()
                save_png(request.data.get('url'))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': "Json is not correct"})
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
        url_list, photos_list_of_dict = get_import_fotos_data()
        if url_list and photos_list_of_dict:
            serializer = PhotoSerializer(data=photos_list_of_dict, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(save_fotos_from_urls(url_list))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "request error"})

    def post(self, request):
        url_list, photos_list_of_dict = get_import_fotos_data(request.data)
        if url_list and photos_list_of_dict:
            serializer = PhotoSerializer(data=photos_list_of_dict, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(save_fotos_from_urls(url_list))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "Json is not correct"})






