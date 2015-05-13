from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from pizza_delivery_app.models import Venue, Cook

__author__ = 'dvpermyakov'


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def cooks_list(request):
    venue = Venue.get_by_username(request.user.username)
    if not venue:
        return HttpResponseForbidden()
    values = {
        'cooks': Cook.objects.filter(venue=venue)
    }
    return render(request, 'web/venue/cooks.html', values)