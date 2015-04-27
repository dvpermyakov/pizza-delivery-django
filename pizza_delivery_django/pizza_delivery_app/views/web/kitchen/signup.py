# coding=utf-8
import logging
from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from pizza_delivery_app.forms import SignUpForm
from pizza_delivery_app.models import Venue, Product
from pizza_delivery_app.models.kitchen import Cook, CookedProduct
from pizza_delivery_app.permissions.groups import COOK_GROUP
from pizza_delivery_app.permissions.methods import add_group, add_permissions
from pizza_delivery_app.permissions.permissions import COOK_PERMISSIONS


class KitchenForm(SignUpForm):
    products = forms.MultipleChoiceField(label='Продукты', required=True)

    def __init__(self, venue, *args, **kwargs):
        super(KitchenForm, self).__init__(*args, **kwargs)
        choices = [(product.id, product.name) for product in venue.get_products_from_menu(venue_product=False)]
        self.fields['products'].choices = choices

    def is_valid(self):
        valid = super(KitchenForm, self).is_valid()
        if not valid:
            return valid
        if len(self.cleaned_data['products']) == 0:
            return False
        return True


def signup(request):
    def general_render(form):
        values = {
            'form': form,
            'title': 'Регистрация новой кофейни'
        }
        values.update(csrf(request))
        return render(request, 'web/signup.html', values)

    venue = Venue.get_by_username(request.user.username)
    if not venue:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return general_render(KitchenForm(venue))
    elif request.method == 'POST':
        form = KitchenForm(venue=venue, data=request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            products = form.cleaned_data['products']

            cook = User.objects.create_user(login, email, password)
            add_group(cook, COOK_GROUP)
            add_permissions(cook, [COOK_PERMISSIONS])

            cook = Cook(venue=venue, cook_name=cook.username)
            cook.save()
            for product_id in products:
                CookedProduct(cook=cook, product=Product.objects.get(id=product_id)).save()

            return redirect('/web/venue/cooks/list/')
        else:
            return general_render(form)