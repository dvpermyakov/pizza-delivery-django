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