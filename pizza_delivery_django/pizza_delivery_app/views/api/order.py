# coding:utf-8
import logging
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.methods.yandex_money import request_payment, process_payment
from pizza_delivery_app.models import Order, OrderProduct
from pizza_delivery_app.models.user import YANDEX_MONEY

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.order.validation import validate_order


@csrf_exempt
def order(request):
    def send_error(description):
        return JsonResponse({
            'success': False,
            'description': description
        })

    logging.error(request.POST)
    try:
        order_obj = json.loads(request.POST.get('order'))
    except ValueError:
        return HttpResponseBadRequest()
    success, _dict = validate_order(order_obj)
    if not success:
        return send_error(_dict.get('description'))
    else:
        order = Order(total_sum=_dict['total_sum'], user=_dict['user'], venue=_dict['venue'])
        venue = _dict['venue']
        company = venue.company
        wallet = _dict['wallet']

        is_payed = False
        if 'wallet' in _dict:
            response = request_payment(wallet.token, order, company)
            if response.get('status') == 'success':
                response = process_payment(response.get('request_id'), wallet.token)
                if response.get('status') == 'success':
                    is_payed = True
                    order.payment_type = YANDEX_MONEY
                    order.payment_id = response.get('payment_id')
                else:
                    return send_error(response.get('error'))
            elif response.get('status') == 'refused':
                return send_error(response.get('error'))

        if not is_payed:
            return send_error(u'Не найден способ оплаты')

        order.save()
        for item_dict in _dict['item_dicts']:
            order_product = OrderProduct(order=order,
                                         venue_product=item_dict['venue_product'],
                                         total_sum=item_dict['total_sum'])
            order_product.save()
        response = {
            'success': success
        }
        response.update(order.dict())
        return JsonResponse(response)


@csrf_exempt
def check_order(request):
    logging.error(request.POST)
    try:
        order_obj = json.loads(request.POST.get('order'))
    except ValueError:
        return HttpResponseBadRequest()
    success, _dict = validate_order(order_obj)
    if not success:
        return JsonResponse({
            'success': success,
            'description': _dict.get('description')
        })
    else:
        return JsonResponse({
            'success': success,
            'total_sum': _dict.get('total_sum')
        })
