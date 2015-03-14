# coding: utf-8

from django.db import models
from pizza_delivery_app.methods import storage_disk


class Company(models.Model):
    name = models.CharField(max_length=255)
    chief_username = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255, null=True)

    @classmethod
    def create(cls, company_name, user, image):
        company = cls(chief_username=user.username, name=company_name)
        company.save()
        storage_disk.create_company_folder(company)
        image_url = storage_disk.upload_company_file(company, storage_disk.COMPANY, company.id, image)
        company.image_url = image_url
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