import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
from .datahandler import create_url_local
import requests


async def save_fotos_from_urls(url_list):
    session = aiohttp.ClientSession()

    async def get(url):
        async with session.get(url+'.png',ssl=False) as responce:
            png_f=Image.open(BytesIO(await responce.read()))
            url_local = create_url_local(url)
            png_f.save(url_local, format='png')
    await asyncio.gather(*(get(url) for url in url_list))
    await session.close()


def save_png(url):
    try:
        with Image.open(BytesIO(requests.get(url+'.png').content)) as png_f:
            url_local = create_url_local(url)
            png_f.save(url_local, format='png')
        return False
    except:
        raise EOFError