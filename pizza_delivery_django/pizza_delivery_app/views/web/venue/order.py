import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from pizza_delivery_app.models import Order, Venue, OrderProduct
from datetime import datetime
from django.shortcuts import render
from pizza_delivery_app.methods.times import timestamp

__author__ = 'Administrator'


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def confirm_order(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest()
    old_status = order.status
    order.confirm()
    return JsonResponse({
        'order_id': order.id,
        'status': Order.STATUS_CHOICES[order.status][1],
        'status_class': Order.STATUS_CHOICES[order.status][0],
        'status_class_old': old_status
    })


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def deliver_order(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest()
    old_status = order.status
    order.deliver()
    return JsonResponse({
        'order_id': order.id,
        'status': Order.STATUS_CHOICES[order.status][1],
        'status_class': Order.STATUS_CHOICES[order.status][0],
        'status_class_old': old_status
    })


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def close_order(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest()
    old_status = order.status
    order.close()
    return JsonResponse({
        'order_id': order.id,
        'status': Order.STATUS_CHOICES[order.status][1],
        'status_class': Order.STATUS_CHOICES[order.status][0],
        'status_class_old': old_status
    })


def _prepare_orders(orders):
    last_time = 0
    for order in orders:
        if timestamp(order.created) > last_time:
            last_time = timestamp(order.created)
        order.status_class = order.status
        order.status = Order.STATUS_CHOICES[order.status][1]
        order.created_time = order.created.strftime('%H:%M:%S')
        order.updated_time = order.updated.strftime('%H:%M:%S')
        order_products = order.get_products()
        for product in order_products:
            product.dict = product.venue_product.product_dict()
            product.status = OrderProduct.STATUS_CHOICES[product.status][1]
        order.products = order_products
        if order.user.address:
            order.user.address_str = order.user.address.to_str()
    return orders, last_time


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def order_list(request):
    venue = Venue.get_by_username(request.user.username)
    if not venue:
        return HttpResponseForbidden()
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    orders = Order.objects.filter(venue=venue, created__gte=today)
    orders, last_time = _prepare_orders(orders)
    values = {
        'orders': orders,
        'last_time': last_time + 1,
        'statuses': [{
            'name': status[1],
            'value': status[0]
        } for status in Order.STATUS_CHOICES]
    }
    values.update(csrf(request))
    return render(request, 'web/venue/orders.html', values)


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def new_orders(request):
    venue = Venue.get_by_username(request.user.username)
    last_time = request.GET.get('last_time')
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    if timestamp(today) > int(last_time):
        last_time = timestamp(today)
    if last_time:
        logging.error(last_time)
        last_time = datetime.utcfromtimestamp(int(last_time))
        orders = Order.objects.filter(created__gt=last_time, venue=venue)
        if orders:
            orders, last_time = _prepare_orders(orders)
            order_dicts = [order.dict() for order in orders]
            for order_dict in order_dicts:
                order_dict.update({
                    'created_time': datetime.utcfromtimestamp(order_dict['created']).strftime('%H:%M:%S'),
                    'updated_time': datetime.utcfromtimestamp(order_dict['updated']).strftime('%H:%M:%S')
                })
                for product in order_dict.get('products', []):
                    if product.get('status') is not None:
                        product['status'] = OrderProduct.STATUS_CHOICES[product['status']][1]
                for status in Order.STATUS_CHOICES:
                    if order_dict.get('status') in status:
                        order_dict.update({
                            'status_class': status[0]
                        })
        else:
            order_dicts = []
            last_time = timestamp(last_time)
        return JsonResponse({
            'orders': order_dicts,
            'last_time': last_time if not order_dicts else last_time + 1
        })
    else:
        return HttpResponseBadRequest()


@login_required
@permission_required('pizza_delivery_app.crud_venues')
def update_statuses(request):
    orders = request.GET.get('orders')
    if not orders:
        return HttpResponseBadRequest()
    orders = orders.split(',')
    response = []
    for order_id_full in orders:
        order_id = order_id_full.split('_')[0].strip()
        status = order_id_full.split('_')[1].strip()
        updated = order_id_full.split('_')[2].strip()
        updated = datetime.strptime(updated, '%H:%M:%S')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest()
        if Order.STATUS_CHOICES[order.status][1] != status or order.updated > updated:
            status_class_old = 0
            for status_tuple in Order.STATUS_CHOICES:
                if status in status_tuple:
                    status_class_old = status_tuple[0]
            response.append({
                'order_id': order_id,
                'status': Order.STATUS_CHOICES[order.status][1],
                'status_class_old': status_class_old,
                'status_class': order.status,
                'products': [{
                    'product_id': product.id,
                    'product_status': OrderProduct.STATUS_CHOICES[product.status][1]
                } for product in order.get_products() if product.status == OrderProduct.COOKED],
            })
    logging.error(response)
    return JsonResponse({
        'orders': response
    })