# coding: utf-8
import logging
from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Venue
from pizza_delivery_app.methods.times import timestamp


def _parse_menu_category(category, venue=None):
    category['products'] = [product.dict(venue) for product in category['products']]
    category['category'] = category['category'].dict()
    category['children'] = [_parse_menu_category(child_category, venue) for child_category in category['children']]
    return category


def menu(request):
    logging.error(request)
    venue_id = request.GET.get('venue_id')
    for_venue_only = 'venue_only' in request.GET
    logging.error(for_venue_only)
    if venue_id:
        venue_id = int(venue_id)
        try:
            venue = Venue.objects.get(id=venue_id)
            if for_venue_only:
                venue_only = venue
            else:
                venue_only = None
            return JsonResponse({
                'menu': _parse_menu_category(venue.get_menu(venue_product=False), venue_only),
                'venues_updated': [venue.updated_dict() for venue in venue.first_category.get_venues()] if not for_venue_only
                else [venue.updated_dict()]
            })
        except Venue.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def last_modified_menu(request):
    venue_id = request.GET.get('venue_id')
    if venue_id:
        venue_id = int(venue_id)
        try:
            venue = Venue.objects.get(id=venue_id)
            return JsonResponse({
                'category_time': timestamp(venue.first_category.updated),
                'venue_time': timestamp(venue.updated)
            })
        except Venue.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()