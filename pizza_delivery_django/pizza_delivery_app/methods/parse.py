# coding=utf-8
import json
import logging
import requests
from pizza_delivery_app.methods.times import timestamp
from datetime import datetime, timedelta
from pizza_delivery_app.models import Order

__author__ = 'dvpermyakov'

PARSE_APPLICATION_ID = 'cgWJAMAhmJeM0RU5J9zWHY5YlutujPZJhi4obcHC'
PARSE_API_KEY = 'Bdqqugqx9OFe3rsc5TDOJuRTPjZGPQonRUIGuhJ7'

IOS_DEVICE = 0
ANDROID_DEVICE = 1

DEVICE_TYPE_MAP = {
    IOS_DEVICE: 'ios',
    ANDROID_DEVICE: 'android'
}

ORDER_TYPE = 0
CLIENT_TYPE = 1
COMPANY_TYPE = 2


def send_push(channels, device_type, data):
    url = 'https://api.parse.com/1/push'
    payload = {
        'channels': channels,
        'type': DEVICE_TYPE_MAP[device_type],
        'expiry': timestamp(datetime.utcnow() + timedelta(days=365)),
        'data': data
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Parse-Application-Id': PARSE_APPLICATION_ID,
        'X-Parse-REST-API-Key': PARSE_API_KEY
    }
    result = requests.post(url, data=json.dumps(payload), headers=headers).text
    logging.error(result)


def get_order_android_data(order):
    return {
        'title': u'Заказ №%s' % order.id,
        'text': u'Ваш заказ был %s' % Order.STATUS_CHOICES[order.status][1],
        'type': ORDER_TYPE,
        'order_id': order.id
    }