from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Venue, Company, Address

__author__ = 'dvpermyakov'


def venues(request):
    company_id = request.GET.get('company_id')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return HttpResponseBadRequest()
    lat = float(lat)
    lon = float(lon)
    address = Address(lat=lat, lon=lon)
    if company_id:
        company = Company.objects.get(id=company_id)
        suited_venues = []
        for venue in Venue.objects.filter(company=company):
            if venue.is_included(address):
                suited_venues.append(venue)
        try:
            return JsonResponse({
                'venues': [venue.dict() for venue in suited_venues]
            })
        except Company.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()