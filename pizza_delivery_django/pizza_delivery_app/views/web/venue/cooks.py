from django.http import HttpResponseForbidden
from django.shortcuts import render
from pizza_delivery_app.models import Venue, Cook

__author__ = 'dvpermyakov'


def cooks_list(request):
    venue = Venue.get_by_username(request.user.username)
    if not venue:
        return HttpResponseForbidden()
    values = {
        'cooks': Cook.objects.filter(venue=venue)
    }
    return render(request, 'web/venue/cooks.html', values)