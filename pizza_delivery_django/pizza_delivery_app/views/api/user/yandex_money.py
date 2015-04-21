# coding: utf-8
import logging
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from pizza_delivery_app.models import User

__author__ = 'dvpermyakov'

from pizza_delivery_app.methods.yandex_money import authorize, get_token


def auth(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    return HttpResponse(authorize(user.id))


def get_token(request):
    code = request.GET.get("code")
    user_id = request.GET.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse()
    response = get_token(code)
    logging.error(response)
    user.yd_token = response["access_token"]
    user.save()
    return HttpResponse()