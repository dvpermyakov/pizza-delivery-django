import logging
from django.core.context_processors import csrf
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from pizza_delivery_app.models import Order, Venue
from datetime import datetime, timedelta
from django.shortcuts import render

__author__ = 'Administrator'


def confirm_order(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest()
    order.confirm()
    return JsonResponse({
        'order_id': order.id,
        'status': order.status
    })


def order_list(request):
    venue = Venue.get_by_username(request.user.username)
    if not venue:
        return HttpResponseForbidden()
    venue.address.timezone_offset = 10800  # TODO: remove it! this is hardcode!
    venue.address.save()
    today = datetime.utcnow().replace(hour=0, minute=0) - timedelta(seconds=venue.address.timezone_offset)
    orders = Order.objects.filter(created__gte=today)
    for order in orders:
        if order.user.address:
            order.user.address_str = order.user.address.to_str()
    values = {
        'orders': orders
    }
    values.update(csrf(request))
    return render(request, 'web/venue/orders.html', values)