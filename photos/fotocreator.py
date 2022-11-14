import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
import requests


async def save_fotos_from_urls(list_of_obj_photos):
    session = aiohttp.ClientSession()

    async def get(url, ph_id):
        async with session.get(url, ssl=False) as responce:
            png_f = Image.open(BytesIO(await responce.read()))
            url_local = 'media/' + str(ph_id) + '.png'
            png_f.save(url_local, format='png')

    await asyncio.gather(*(
        get('https://via.placeholder.com/' + str(ph_dict['width']) + 'x' + str(ph_dict['height']) + '/' + ph_dict[
            'dominant_color'] + '.png', ph_dict['id'])
        for ph_dict in list_of_obj_photos))
    await session.close()


def save_png(url,ph_id):
    try:
        with Image.open(BytesIO(requests.get(url + '.png').content)) as png_f:
            url_local = 'media/' + str(ph_id) + '.png'
            png_f.save(url_local, format='png')
        return False
    except:
        raise EOFError
