# coding=utf-8
from django.db import models
from pizza_delivery_app.models import Product, Venue, OrderProduct

__author__ = 'dvpermyakov'


class Cook(models.Model):
    venue = models.ForeignKey(Venue)
    cook_name = models.CharField(max_length=255)

    @classmethod
    def get_cook_by_username(cls, username):
        return cls.objects.get(cook_name=username)

    @classmethod
    def get_cook_by_order_product(cls, ordered_product):
        cooks = [product.cook
                 for product in CookedProduct.objects.filter(product=ordered_product.venue_product.product)]
        if cooks:
            return cooks[0]
        else:
            return None


class CookedProduct(models.Model):
    cook = models.ForeignKey(Cook, null=True)
    product = models.ForeignKey(Product)


class CookedOrderedProduct(models.Model):
    NEW = 0
    COOKED = 1

    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (COOKED, u'Приготовлен')
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)
    cook = models.ForeignKey(Cook, null=True)
    product = models.OneToOneField(OrderProduct)

    def set_cooked(self):
        self.status = self.COOKED
        self.save()

    def dict(self):
        return {
            'id': self.id,
            'number': self.product.id,
            'status': self.status,
            'status_name': self.STATUS_CHOICES[self.status][1],
            'name': self.product.venue_product.product.name
        }