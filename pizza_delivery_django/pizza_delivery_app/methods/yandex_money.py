# coding: utf-8
import logging
import requests

__author__ = 'dvpermyakov'

API_KEY = "DE22D347E583338B9618CF5D8770628F0CB7C7309A14CC9528CC4A6BF4940890"
AUTH_BASE_URL = "http://sp-money.yandex.ru"
BASE_URL = "https://money.yandex.ru"

SCOPES = [
    'account-info',
    'operation-history',
    #'operation-details',
    #'incoming-transfers',
    #'payment'
    #'payment-shop',
    'payment-p2p',
    #'money-source'
]


def authorize(user_id):
    url = AUTH_BASE_URL + "/oauth/authorize"
    params = {
        "client_id": API_KEY,
        "response_type": "code",
        "redirect_uri": "http://92.63.104.244:8080/api/user/card/success?user_id=%s" % user_id,
        "scope": ' '.join(SCOPES)
    }
    logging.error(' '.join(SCOPES))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(url, params=params, headers=headers).text


def get_token(code):
    url = AUTH_BASE_URL + "/oauth/token"
    params = {
        "client_id": API_KEY,
        "redirect_uri": "http://92.63.104.244:8080/api/user/card/success",
        "grant_type": "authorization_code",
        "code": code
    }
    return requests.post(url, params=params).json()


def account_info(token):
    url = BASE_URL + "/api/account-info"
    headers = {
        'Authorization': 'Bearer %s' % token
    }
    return requests.post(url, headers=headers).json()


def request_payment(token, order, company):
    url = BASE_URL + "/api/request-payment"
    params = {
        "pattern_id": "p2p",
        "to": company.yd_wallet_number,
        "amount": order.total_sum,
        "comment": u"Платеж к опании %s за заказ №%s" % (company.name, order.id),
        "message": u"Платеж копании %s за заказ №%s" % (company.name, order.id),
        "label": order.id
    }
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=params)
    return response.json()


def process_payment(request_id, token):
    url = BASE_URL + "/api/process-payment"
    params = {
        "request_id": request_id,
        "money_source": "wallet",
    }
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=params)
    return response.json()