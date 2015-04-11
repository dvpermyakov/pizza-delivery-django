import requests

__author__ = 'dvpermyakov'


def upload_image(file_):
    url = 'http://deviantsart.com'
    response = requests.post(url, files={
        'file': file_
    }).json()
    return response.get('url')