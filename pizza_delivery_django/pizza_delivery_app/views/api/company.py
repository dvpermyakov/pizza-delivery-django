import logging
from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Venue, Address

__author__ = 'dvpermyakov'


def companies(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return HttpResponseBadRequest()
    lat = float(lat)
    lon = float(lon)
    address = Address(lat=lat, lon=lon)
    venues = Venue.objects.all()
    suited_companies = []
    for venue in venues:
        if venue.company not in suited_companies and venue.is_included(address):
            if venue.company not in suited_companies:
                suited_companies.append(venue.company)
    return JsonResponse({
        'companies': [company.dict() for company in suited_companies]
    })