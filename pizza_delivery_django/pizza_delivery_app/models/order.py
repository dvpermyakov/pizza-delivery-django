from django.db import models
from pizza_delivery_app.models import VenueProduct

__author__ = 'dvpermyakov'


class Order(models.Model):
    pass


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_product')
    venue_product = models.ForeignKey(VenueProduct)
    #revenue = models.IntegerField()