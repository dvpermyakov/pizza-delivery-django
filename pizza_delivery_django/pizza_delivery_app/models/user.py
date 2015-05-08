from django.db import models
from pizza_delivery_app.models import Address, Product

__author__ = 'dvpermyakov'

CASH = -1
YANDEX_MONEY = 0

PAYMENT_TYPES = [
    CASH,
    YANDEX_MONEY
]


class User(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.ForeignKey(Address, null=True)

    def dict(self):
        return {
            'id': self.id,
            'address': self.address.dict() if self.address else None,
            'address_str': self.address.to_str() if self.address else None,
            'name': self.name
        }


class YdWallet(models.Model):
    user = models.ForeignKey(User, related_name='yd_wallet')
    token = models.CharField(max_length=2000)
    number = models.CharField(max_length=2000, null=True)

    def dict(self):
        return {
            'number': self.number
        }


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='rating')
    rating = models.FloatField()
    product = models.ForeignKey(Product)

    @staticmethod
    def get_product_rating(product):
        ratings = Rating.objects.filter(product=product)
        return sum([rating.rating for rating in ratings]) / float(len(ratings)) if ratings else 0.0, len(ratings)

    def dict(self):
        return {
            'user_id': self.user.id,
            'rating': self.rating,
            'product_id': self.product.id
        }