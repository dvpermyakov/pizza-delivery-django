# coding:utf-8
import logging

__author__ = 'dvpermyakov'

import requests

CITY = 0
STREET = 1
HOME = 2


def _parse_collection(collection, kind='house'):  # used only for kind in ['house', 'street']
    if kind not in ['house', 'street', 'locality']:
        return
    candidates = []
    for item in collection:
        item = item['GeoObject']
        if item['metaDataProperty']['GeocoderMetaData']['kind'] != kind:
            continue
        address = item['metaDataProperty']['GeocoderMetaData']['AddressDetails']
        country = address['Country']
        if country.get('AdministrativeArea'):
            area = country['AdministrativeArea']
        else:
            continue
        if area.get('SubAdministrativeArea'):
            address = area['SubAdministrativeArea']['Locality']
        else:
            continue
        candidates.append({
            'address': {
                'country': country['CountryName'],
                'city': address['LocalityName'],
                'street': address['Thoroughfare']['ThoroughfareName'].replace(u'улица', '').strip()
                if kind == 'house' or kind == 'street' else None,
                'home': address['Thoroughfare']['Premise']['PremiseNumber'] if kind == 'house' else None
            },
            'coordinates': {
                'lon': item['Point']['pos'].split(' ')[0],
                'lat': item['Point']['pos'].split(' ')[1],
            }
        })
    return candidates


def get_houses_by_address(city, street, home):
    params = {
        'geocode': ('%s,%s,%s' % (city, street, home)).encode('utf-8'),
        'format': 'json',
        'results': 3
    }
    url = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url, params=params).json()
    collection = response['response']['GeoObjectCollection']['featureMember']

    return _parse_collection(collection, kind='house')


def get_houses_by_coordinates(lat, lon):
    params = {
        'geocode': '%s,%s' % (lon, lat),
        'format': 'json',
        'kind': 'house',
        'results': 3
    }
    url = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url, params=params).json()
    collection = response['response']['GeoObjectCollection']['featureMember']

    return _parse_collection(collection, kind='house')


def get_streets_by_address(city, street):
    params = {
        'geocode': ('%s,%s' % (city, street)).encode('utf-8'),
        'format': 'json',
        'kind': 'street',
        'results': 3
    }
    url = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url, params=params).json()
    collection = response['response']['GeoObjectCollection']['featureMember']

    return _parse_collection(collection, kind='street')


def get_cities_by_address(city):
    params = {
        'geocode': ('%s' % city).encode('utf-8'),
        'format': 'json',
        'kind': 'locality',
        'results': 3
    }
    url = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url, params=params).json()
    collection = response['response']['GeoObjectCollection']['featureMember']
    return _parse_collection(collection, kind='locality')