# coding: utf-8
import logging
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from pizza_delivery_app.models import User

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.yandex_money import authorize, get_token, account_info


def auth(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    return HttpResponse(authorize(user.id))


def set_token(request):
    code = request.GET.get('code')
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse()

    user.yd_token = get_token(code)['access_token']
    user.save()
    return HttpResponse('Успешно!')


def get_balance(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    response = account_info(user.yd_token)
    return JsonResponse({
        'account': response['account'],
        'balance': response['balance']
    })