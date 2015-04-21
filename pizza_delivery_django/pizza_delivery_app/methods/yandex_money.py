import logging
import requests
import json

__author__ = 'dvpermyakov'

API_KEY = "DE22D347E583338B9618CF5D8770628F0CB7C7309A14CC9528CC4A6BF4940890"
BASE_URL = "http://m.sp-money.yandex.ru"


def authorize(user_id):
    url = BASE_URL + "/oauth/authorize"
    params = {
        "client_id": API_KEY,
        "response_type": "code",
        "redirect_uri": "http://92.63.104.244:8080/api/user/card/success?user_id=%s" % user_id,
        "scope": "account-info operation-history"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(url, params=params, headers=headers).text


def get_token(code):
    url = BASE_URL + "/oauth/token"
    params = {
        "client_id": API_KEY,
        "redirect_uri": "http://92.63.104.244:8080/api/user/card/success",
        "grant_type": "authorization_code",
        "code": code
    }
    return json.loads(requests.post(url, params=params).json())
