# coding: utf-8
from django.db import models
from pizza_delivery_app.models import VenueProduct, User, Venue
from pizza_delivery_app.methods.times import timestamp

__author__ = 'dvpermyakov'


class Order(models.Model):
    NEW = 0
    CONFIRMED = 1
    COOKING = 2
    DELIVERING = 3
    CLOSED = 4

    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (CONFIRMED, u'был подтвержден'),
        (COOKING, u'готовится'),
        (DELIVERING, u'доставляется'),
        (CLOSED, u'был закрыт')
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    venue = models.ForeignKey(Venue)
    user = models.ForeignKey(User)
    total_sum = models.IntegerField()
    payment_type = models.IntegerField()
    payment_id = models.CharField(max_length=2000)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

    def _change_status(self):
        from pizza_delivery_app.methods import parse
        parse.send_push(channels=['order_%s' % self.id], device_type=parse.ANDROID_DEVICE,
                        data=parse.get_order_android_data(self))

    def dict(self):
        return {
            'order_id': self.id,
            'created': timestamp(self.created),
            'total_sum': self.total_sum,
            'products': [product.dict() for product in OrderProduct.objects.filter(order=self)],
            'status': self.status
        }

    def confirm(self):
        if self.status == self.NEW:
            self.status = self.CONFIRMED
            self._change_status()
            self.save()

    def start_cook(self):
        if self.status == self.CONFIRMED:
            self.status = self.COOKING
            self._change_status()
            self.save()


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