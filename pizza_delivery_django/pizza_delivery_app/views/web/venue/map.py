from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from pizza_delivery_app.models.venue import Venue
from pizza_delivery_app.models.company import Company


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def map_venues(request):
    return render(request, 'web/venue/map.html', {
        'venues': Venue.objects.filter(company=Company.get_by_username(request.user.username))
    })