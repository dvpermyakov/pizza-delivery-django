# coding:utf-8
import logging
from pizza_delivery_app.models import VenueProduct, User, YdWallet
from pizza_delivery_app.models.user import PAYMENT_TYPES, YANDEX_MONEY

__author__ = 'dvpermyakov'


def error(description):
    return False, {
        'description': description
    }


def _validate_products(products):
    if not products:
        return error(u'Неверный формат списка продуктов')
    total_sum = 0
    item_dicts = []
    venue = None
    for product in products:
        try:
            venue_product = VenueProduct.objects.get(id=product.get('venue_product_id'))
            venue = venue_product.venue
            total_sum += venue_product.price
            item_dicts.append({
                'total_sum': venue_product.price,
                'venue_product': venue_product
            })
        except VenueProduct.DoesNotExist:
            return error(u'Неверный формат продукта')
    if not venue:
        return error(u'Невозможно определить кофейню')
    return True, {
        'total_sum': total_sum,
        'item_dicts': item_dicts,
        'venue': venue
    }


def validate_order(order):
    result = {}
    if order.get('payment_type'):
        payment_type = order['payment_type']
        if payment_type.get('type') is not None:
            _type = payment_type['type']
            if _type not in PAYMENT_TYPES:
                return error(u'Недоступный способ оплаты')
            if _type == YANDEX_MONEY:
                try:
                    wallet = YdWallet.objects.get(number=payment_type.get('number'))
                    result.update({
                        'wallet': wallet
                    })
                except YdWallet.DoesNotExist:
                    return error(u'Кошелек не найден')
        else:
            return error(u'Необходимо выбрать способ оплаты')
    if order.get('user'):
        user = order['user']
        try:
            user_obj = User.objects.get(id=user.get('id'))
            result.update({
                'user': user_obj
            })
        except User.DoesNotExist:
            return error(u'Неправильное присвоение id')
    else:
        return error(u'Неавторизованный пользователь')
    if order.get('products'):
        success, _dict = _validate_products(order['products'])
        if not success:
            return success, _dict
        result.update(_dict)
        logging.error(result)
        return success, result
    else:
        return error(u'Неверный формат заказа')