from django.db import models
from pizza_delivery_app.models import Product, Venue

__author__ = 'dvpermyakov'


class Cook(models.Model):
    venue = models.ForeignKey(Venue)
    cook_name = models.CharField(max_length=255)

    @classmethod
    def get_cook_by_username(cls, username):
        return cls.objects.get(cook_name=username)


class CookedProduct(models.Model):
    cook = models.ForeignKey(Cook)
    product = models.ForeignKey(Product)