# coding: utf-8

from django.db import models
from pizza_delivery_app.methods.deviantsart import upload_image


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    chief_username = models.CharField(max_length=255)
    image_url = models.URLField(max_length=1000, null=True)

    @classmethod
    def create(cls, company_name, user, image):
        company = cls(chief_username=user.username, name=company_name)
        company.image_url = upload_image(image)
        company.save()
        return company

    @classmethod
    def get_by_username(cls, username):
        try:
            return cls.objects.get(chief_username=username)
        except Company.DoesNotExist:
            from venue import Venue
            try:
                return Venue.objects.get(manager_username=username).company
            except Venue.DoesNotExist:
                return None

    def dict(self):
        return {
            'name': self.name,
            'image': self.image_url
        }