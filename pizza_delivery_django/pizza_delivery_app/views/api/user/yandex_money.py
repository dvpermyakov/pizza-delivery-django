# coding: utf-8
import logging
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from pizza_delivery_app.models import User, Company
from pizza_delivery_app.models.order import Order
from pizza_delivery_app.models.user import YdWallet

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.yandex_money import authorize, get_token, account_info, request_payment


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

    token = get_token(code)['access_token']
    number = account_info(token)['account']
    YdWallet(user=user, token=token, number=number).save()
    return HttpResponse('Успешно!')


def get_balance(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    wallets = YdWallet.objects.filter(user=user)
    result = []
    for wallet in wallets:
        response = account_info(wallet.token)
        result.append({
            'account': response['account'],
            'balance': response['balance']
        })
    return JsonResponse({
        'info':result
    })


def pay_yd(request):
    user = User.objects.get(id=20)
    company = Company.objects.get(id=1)
    order = Order()
    order.id = 2
    response = request_payment(user.token, order, company)
    return JsonResponse(response)