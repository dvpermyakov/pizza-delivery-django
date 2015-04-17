import logging
from django.http import JsonResponse
from pizza_delivery_app.models.user import User
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.methods import map

__author__ = 'dvpermyakov'


@csrf_exempt
def create_or_update(request):
    def save_address(user, candidates):
        if candidates:
            address = candidates[0].get('address')
            if address:
                user.address.city = address.get('city')
                user.address.street = address.get('street')
                user.address.home = address.get('home')
                user.address.lat = float(lat)
                user.address.lon = float(lon)
                user.address.save()

    logging.error(request.POST)
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None
    name = request.POST.get('name')
    if user:
        user.name = name
    else:
        user = User(name=name)
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')
    save_address(user, map.get_houses_by_coordinates(lat, lon))
    user.save()
    return JsonResponse(user.dict())