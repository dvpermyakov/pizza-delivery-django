# coding:utf-8
from pizza_delivery_app.models import VenueProduct

__author__ = 'dvpermyakov'


def error(description):
    return False, {
        'description': description
    }


def _validate_products(products):
    if not products:
        return error(u'Неверный формат списка продуктов')
    total_sum = 0
    for product in products:
        try:
            venueProduct = VenueProduct.objects.get(product.get('venue_product_id'))
            total_sum += venueProduct.price
        except VenueProduct.DoesNotExist:
            return error(u'Неверный формат продукта')
        return True, {
            'total_sum': total_sum
        }


def validate_order(order):
    if order.get('products'):
        success, _dict = _validate_products(order['products'])
        if not success:
            return success, _dict
        return success, _dict
    else:
        return error(u'Неверный формат заказа')