import logging
from django.http import JsonResponse
from pizza_delivery_app.models import Address
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
                logging.error("It should be changed")
                if not user.address:
                    address_obj = Address()
                else:
                    address_obj = user.address
                address_obj.city = address.get('city')
                address_obj.street = address.get('street')
                address_obj.home = address.get('home')
                address_obj.lat = float(lat)
                address_obj.lon = float(lon)
                address_obj.save()
                user.address = address_obj

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
    if user.address:
        logging.error(user.address.id)
    return JsonResponse(user.dict())