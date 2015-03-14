# coding: utf-8
from django.http import JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import Company
import logging


def _parse_menu_category(category):
    category['products'] = [product.dict() for product in category['products']]
    if not category['products']:
        del category['products']
    category['category'] = category['category'].dict()
    category['children'] = [_parse_menu_category(child_category) for child_category in category['children']]
    if not category['children']:
        del category['children']
    return category


def menu(request):
    company_id = request.GET.get('company_id')
    if company_id:
        company_id = int(company_id)
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

    return JsonResponse({
        'menu': _parse_menu_category(company.get_menu())
    })