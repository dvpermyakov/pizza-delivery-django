# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
from pizza_delivery_app.models import Company, Venue


@login_required
def main_page(request):
    user = request.user
    company = Company.get_by_username(user.username)
    venues = Venue.objects.filter(company=company)
    for venue in venues:
        venue.address_name = venue.address.to_str()
        venue.status = u'Открыто'
    return render(request, 'web/company/main.html', {
        'user': user,
        'venues': venues
    })