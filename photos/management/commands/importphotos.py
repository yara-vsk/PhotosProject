from django.core.management.base import BaseCommand, CommandError
from photos.serializers import PhotoSerializer
from photos.datahandler import get_import_fotos_data
from photos.fotocreator import save_fotos_from_urls
import asyncio
import json



class Command(BaseCommand):
    help = 'Importphotos'

    def add_arguments(self, parser):
        parser.add_argument('Import from', type=str)
        parser.add_argument('json_file', type=str)



    def handle(self, *args, **options):
        if options['Import from']=='api':
            self.get_from_api()
            return
        elif options['Import from']=='json':
            if options['json_file']:
                self.get_from_json(options['json_file'])
                return
            raise CommandError('missing json file')
        else:
            raise CommandError('Enter as argument "api" or "json"')

    def get_from_api(self):
        url_list, photos_list_of_dict = get_import_fotos_data()
        if url_list and photos_list_of_dict:
            serializer = PhotoSerializer(data=photos_list_of_dict, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(save_fotos_from_urls(url_list))
                    self.stdout.write('Import photos from external API is success')
                    return
                except:
                    raise CommandError('Error')
            raise CommandError('Error')
        raise CommandError('Error')

    def get_from_json(self, json_f):
        url_list, photos_list_of_dict = get_import_fotos_data(json.loads(json_f))
        if url_list and photos_list_of_dict:
            serializer = PhotoSerializer(data=photos_list_of_dict, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(save_fotos_from_urls(url_list))
                    self.stdout.write('Import photos from json is success')
                    return
                except:
                    raise CommandError('Error')
            raise CommandError('Error')
        raise CommandError('Error')
