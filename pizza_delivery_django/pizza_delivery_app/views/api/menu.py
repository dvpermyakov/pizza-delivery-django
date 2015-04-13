# coding: utf-8
from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Venue


def _parse_menu_category(category):
    category['products'] = [product.dict() for product in category['products']]
    category['category'] = category['category'].dict()
    category['children'] = [_parse_menu_category(child_category) for child_category in category['children']]
    return category


def menu(request):
    venue_id = request.GET.get('venue_id')
    if venue_id:
        venue_id = int(venue_id)
        try:
            venue = Venue.objects.get(id=venue_id)
            return JsonResponse({
                'menu': _parse_menu_category(venue.get_menu(venue_product=False))
            })
        except Venue.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()