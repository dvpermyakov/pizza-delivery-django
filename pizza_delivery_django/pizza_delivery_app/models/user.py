from django.db import models
from pizza_delivery_app.models import Address

__author__ = 'dvpermyakov'


class User(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, null=True)

    def dict(self):
        return {
            'id': self.id,
            'address': self.address.dict() if self.address else None,
            'name': self.name
        }