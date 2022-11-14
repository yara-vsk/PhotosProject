import re
import requests


def get_data_from_url(url):
    url = url + '.png'
    png_f_width = None
    png_f_heigth = None
    png_f_dominate_color = None
    width = re.search(r'/[0-9]{1,4}/', url)
    if width:
        png_f_width = int(url[width.start() + 1:width.end() - 1])
        png_f_heigth = png_f_width
    else:
        width = re.search(r'/[0-9]{1,4}x', url)
        heigth = re.search(r'x[0-9]{1,4}/', url)
        if width and heigth:
            png_f_width = int(url[width.start() + 1:width.end() - 1])
            png_f_heigth = int(url[heigth.start() + 1:heigth.end() - 1])
    color = re.search(r'/[0-9a-fA-F]{3,6}.png$', url)
    if color:
        png_f_dominate_color = url[color.start() + 1:-4]
    if png_f_width and png_f_heigth and png_f_dominate_color:
        return (png_f_width, png_f_heigth, png_f_dominate_color)
    return False


def get_import_fotos_data(request_data=None):
    photos_list_of_dict = []
    if request_data is None:
        try:
            photos_list = requests.get('https://jsonplaceholder.typicode.com/photos').json()
            for photo_dict in photos_list:
                data_list = get_data_from_url(photo_dict.get('url'))
                if data_list:
                    photo_dict['width'] = data_list[0]
                    photo_dict['height'] = data_list[1]
                    photo_dict['dominant_color'] = data_list[2]
                    photos_list_of_dict.append(photo_dict)
            return photos_list_of_dict
        except:
            return None

    try:
        photos_list = request_data
        for photo_dict in photos_list:
            data_list = get_data_from_url(photo_dict.get('url'))
            if data_list:
                photo_dict['width'] = data_list[0]
                photo_dict['height'] = data_list[1]
                photo_dict['dominant_color'] = data_list[2]
                photos_list_of_dict.append(photo_dict)
        return photos_list_of_dict
    except:
        return None


def get_import_foto_data(request_data):
    data_list = get_data_from_url(request_data.get('url'))
    if data_list:
        request_data['width'] = data_list[0]
        request_data['height'] = data_list[1]
        request_data['dominant_color'] = data_list[2]
        return request_data
    return None



