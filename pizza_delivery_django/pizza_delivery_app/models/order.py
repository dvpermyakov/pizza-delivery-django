# coding: utf-8
from django.db import models
from pizza_delivery_app.models import VenueProduct, User, Venue
from pizza_delivery_app.methods.times import timestamp

__author__ = 'dvpermyakov'


class Order(models.Model):
    NEW = 0
    CONFIRMED = 1
    COOKING = 2
    COOKED = 3
    DELIVERING = 4
    CLOSED = 5

    STATUS_CHOICES = (
        (NEW, u'новый'),
        (CONFIRMED, u'был подтвержден'),
        (COOKING, u'готовится'),
        (COOKED, U'был приготовлен'),
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
            'updated': timestamp(self.updated),
            'total_sum': self.total_sum,
            'products': [product.dict() for product in OrderProduct.objects.filter(order=self)],
            'status': self.status,
            'user': self.user.dict()
        }

    def get_products(self):
        return OrderProduct.objects.filter(order=self)

    def confirm(self):
        from pizza_delivery_app.models import Cook, CookedOrderedProduct
        if self.status == self.NEW:
            self.status = self.CONFIRMED
            for product in OrderProduct.objects.filter(order=self):
                CookedOrderedProduct(product=product, cook=Cook.get_cook_by_order_product(product)).save()
            self._change_status()
            self.save()

    def deliver(self):
        if self.status == self.COOKED:
            self.status = self.DELIVERING
            self._change_status()
            self.save()

    def close(self):
        if self.status == self.DELIVERING:
            self.status = self.CLOSED
            self._change_status()
            self.save()

    def check_status_after_cooking(self):
        self.save()
        if self.status == self.CONFIRMED:
            self.status = self.COOKING
            self.save()
        for product in self.order_product.all():
            if product.status == OrderProduct.NEW:
                return
        self.status = self.COOKED
        self._change_status()
        self.save()


class OrderProduct(models.Model):
    NEW = 0
    COOKED = 1

    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (COOKED, u'Приготовлен')
    )

    order = models.ForeignKey(Order, related_name='order_product')
    venue_product = models.ForeignKey(VenueProduct)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)
    total_sum = models.IntegerField()

    def cook(self):
        if self.status == self.NEW:
            self.status = self.COOKED
            self.save()
        self.order.check_status_after_cooking()

    def dict(self):
        dict = self.venue_product.product_dict()
        dict.update({
            'order_product_id': self.id,
            'total_sum': self.total_sum,
            'status': self.status
        })
        return dict