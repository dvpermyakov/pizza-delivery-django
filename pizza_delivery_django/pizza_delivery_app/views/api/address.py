from django.http import HttpResponseBadRequest, JsonResponse

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods import map


def get_home_by_coordinates(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    try:
        candidates = map.get_houses_by_coordinates(lat, lon)
        if candidates:
            return JsonResponse({
                'success': True,
                'address': candidates[0]['address']
            })
        else:
            return JsonResponse({
                'success': False
            })
    except:
        return HttpResponseBadRequest()


def get_coordinates_by_home(request):
    city = request.GET.get('city')
    street = request.GET.get('street')
    home = request.GET.get('home')
    try:
        candidates = map.get_houses_by_address(city, street, home)
        if candidates:
            return JsonResponse({
                'success': True,
                'lat': candidates[0].get('coordinates').get('lat'),
                'lon': candidates[0].get('coordinates').get('lon'),
            })
        else:
            return JsonResponse({
                'success': False
            })
    except:
        return HttpResponseBadRequest()


def autocomplete_address(request):
    def get_candidates(candidates):
        addresses = []
        for candidate in candidates:
            if candidate.get('address'):
                addresses.append(candidate['address'])
        return addresses

    string = request.GET.get('string')
    if not string:
        return JsonResponse({
            'addresses': []
        })
    type = int(request.GET.get('type'))
    if type == map.CITY:
        return JsonResponse({
            'addresses': get_candidates(map.get_cities_by_address(string))
        })
    elif type == map.STREET:
        string = string.split(',')
        return JsonResponse({
            'addresses': get_candidates(map.get_streets_by_address(string[0], string[1]))
        })
    elif type == map.HOME:
        string = string.split(',')
        return JsonResponse({
            'addresses': get_candidates(map.get_houses_by_address(string[0], string[1], string[2]))
        })