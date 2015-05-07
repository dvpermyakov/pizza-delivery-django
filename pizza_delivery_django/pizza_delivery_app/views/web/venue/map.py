import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from pizza_delivery_app.models import GeoPoint, GeoRib
from pizza_delivery_app.models.venue import Venue
from pizza_delivery_app.models.company import Company


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def map_venues(request):
    return render(request, 'web/venue/map.html', {
        'venues': Venue.objects.filter(company=Company.get_by_username(request.user.username))
    })


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def restriction_map(request):
    if request.method == 'GET':
        venue_id = request.GET.get('venue_id')
        try:
            venue = Venue.objects.get(id=venue_id)
        except Venue.DoesNotExist:
            return HttpResponseBadRequest()
        values = {
            'lat': venue.address.lat,
            'lon': venue.address.lon,
            'name': venue.name,
            'coords': venue.first_rib.get_polygon() if venue.first_rib else []
        }
        values.update(csrf(request))
        return render(request, 'web/venue/restriction_map.html', values)
    elif request.method == 'POST':
        logging.error(request.POST)
        venue_id = request.GET.get('venue_id')
        try:
            venue = Venue.objects.get(id=venue_id)
        except Venue.DoesNotExist:
            return HttpResponseBadRequest()
        polygon = request.POST.get('polygon').split(',')
        polygon = [point for point in polygon if point]

        def get_point(index, rib):
            lat = float(polygon[index])
            index += 1
            lon = float(polygon[index])
            index += 1
            point = GeoPoint(lat=lat, lon=lon, rib=rib)
            point.save()
            return point, index

        i = 0
        rib = GeoRib()
        rib.save()
        point, i = get_point(i, rib)
        point, i = get_point(i, rib)
        venue.first_rib = rib
        venue.save()
        while i < len(polygon):
            rib = GeoRib(parent=rib)
            rib.save()
            GeoPoint(lat=point.lat, lon=point.lon, rib=rib).save()
            point, i = get_point(i, rib)
        return redirect('/web/company/main')