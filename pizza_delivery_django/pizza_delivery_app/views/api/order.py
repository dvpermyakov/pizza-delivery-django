import logging
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt
from pizza_delivery_app.models import Order, OrderProduct

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.order.validation import validate_order


@csrf_exempt
def order(request):
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
        order = Order(total_sum=_dict['total_sum'], user=_dict['user'], venue=_dict['venue'])
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
