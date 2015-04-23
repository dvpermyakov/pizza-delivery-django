import logging
from django.http import JsonResponse, HttpResponseBadRequest
import json

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.order.validation import validate_order, validate_products


def order(request):
    logging.error(request.POST)
    order = request.POST.get('order')
    success, _dict = validate_order(order)
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


def check_order(request):
    logging.error(request.POST)
    order = request.POST.get('order')
    success, _dict = validate_order(order)
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