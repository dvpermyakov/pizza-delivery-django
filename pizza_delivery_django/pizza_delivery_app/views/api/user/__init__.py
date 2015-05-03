__author__ = 'dvpermyakov'

from registration import create_or_update
from yandex_money import auth, set_token, get_balance, pay_yd
from payments import available_payment_types
from history import order_history
from rating import set_rating