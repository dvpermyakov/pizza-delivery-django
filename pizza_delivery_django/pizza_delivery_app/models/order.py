from django.db import models
from pizza_delivery_app.models import VenueProduct, User, Venue
from pizza_delivery_app.methods.times import timestamp

__author__ = 'dvpermyakov'


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    venue = models.ForeignKey(Venue)
    user = models.ForeignKey(User)
    total_sum = models.IntegerField()

    def dict(self):
        return {
            'order_id': self.id,
            'created': timestamp(self.created),
            'total_sum': self.total_sum,
            'products': [product.dict() for product in OrderProduct.objects.filter(order=self)]
        }


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_product')
    venue_product = models.ForeignKey(VenueProduct)
    total_sum = models.IntegerField()

    def dict(self):
        dict = self.venue_product.dict(product_include=False)
        dict.update({
            'total_sum': self.total_sum
        })
        return dict