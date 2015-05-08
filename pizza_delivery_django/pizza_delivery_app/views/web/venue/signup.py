# coding: utf-8

from django.core.context_processors import csrf
from django.forms.util import ErrorList
from pizza_delivery_app.forms import SignUpForm
from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from pizza_delivery_app.methods import map
from pizza_delivery_app.models.address import Address
from pizza_delivery_app.models.venue import Venue, VenueProduct
from pizza_delivery_app.models.menu import Category
from pizza_delivery_app.models.company import Company
from pizza_delivery_app.permissions.groups import MANAGER_GROUP, MENU_READ_PERMISSIONS
from pizza_delivery_app.permissions.methods import add_group, add_permissions
from django.contrib.auth.decorators import login_required, permission_required
from pizza_delivery_app.methods.google_api import get_timezone


class VenueSignUpForm(SignUpForm):
    city = forms.CharField(label=u'Город', max_length=40, widget=forms.TextInput(attrs={
        'readonly': 'readonly'
    }))
    street = forms.CharField(label=u'Улица', max_length=40, widget=forms.TextInput(attrs={
        'readonly': 'readonly'
    }))
    home = forms.CharField(label=u'Дом', max_length=40, widget=forms.TextInput(attrs={
        'readonly': 'readonly'
    }))
    venue_name = forms.CharField(label=u'Название кофейни', max_length=40)
    description = forms.CharField(label=u'Описание кофейни', widget=forms.Textarea())
    first_category = forms.ChoiceField(label=u'Загрузить меню из другой кофейни')

    def __init__(self, company=None, *args, **kwargs):
        super(VenueSignUpForm, self).__init__(*args, **kwargs)
        choices = [
            (0, u'Собственное меню'),
        ]
        if company:
            choices.extend(
                [(venue.id, venue.name) for venue in Venue.objects.filter(company=company)],
            )
        self.fields['first_category'].choices = choices

    def is_valid(self):
        valid = super(VenueSignUpForm, self).is_valid()
        if not valid:
            return valid
        if Venue.objects.filter(name=self.cleaned_data['venue_name']).count() > 0:
            self._errors['venue_name'] = ErrorList([u'Кофейня с таким именем уже существует'])
            return False
        return True


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def signup(request):
    def general_render(form):
        values = {
            'form': form,
            'title': 'Регистрация новой кофейни'
        }
        values.update(csrf(request))
        return render(request, 'web/signup.html', values)

    company = Company.get_by_username(request.user.username)
    if not company:
        return HttpResponseForbidden()

    lat, lon = float(request.GET['lat']), float(request.GET['lon'])
    houses = map.get_houses_by_coordinates(lat, lon)
    if not houses:
        return render(request, 'web/venue/map.html')

    if request.method == 'GET':
        return general_render(VenueSignUpForm(company=company, initial={
            'city': houses[0]['address']['city'],
            'street': houses[0]['address']['street'],
            'home': houses[0]['address']['home'],
        }))
    elif request.method == 'POST':
        form = VenueSignUpForm(company=company, data=request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            venue_name = form.cleaned_data['venue_name']
            description = form.cleaned_data['description']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            home = form.cleaned_data['home']

            address = Address(city=city, street=street, home=home, lat=lat, lon=lon)
            response = get_timezone(address)
            if response.get('status') == "OK":
                address.timezone_offset = response.get('rawOffset')
                address.timezone_id = response.get('timeZoneId')
                address.timezone_name = response.get('timeZoneName')

            address.save()

            manager = User.objects.create_user(login, email, password)
            add_group(manager, MANAGER_GROUP)
            add_permissions(manager, [MENU_READ_PERMISSIONS])
            try:
                copy_venue = Venue.objects.get(id=form.cleaned_data['first_category'])
                first_category = copy_venue.first_category
            except Venue.DoesNotExist:
                first_category = None

            Venue.create(company=company, address=address, name=venue_name, description=description,
                         manager_username=manager.username, first_category=first_category)
            return redirect('/web/venue/map')
        else:
            return general_render(form)