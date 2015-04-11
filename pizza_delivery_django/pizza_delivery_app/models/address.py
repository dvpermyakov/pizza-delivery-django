from django.db import models


class Address(models.Model):
    lat = models.FloatField(max_length=255)
    lon = models.FloatField(max_length=255)

    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    home = models.CharField(max_length=255)

    def to_str(self):
        return '%s, %s, %s' % (self.city, self.street, self.home)

    def dict(self):
        return {
            'lat': self.lat,
            'lon': self.lon,
            'city': self.city,
            'street': self.street,
            'home': self.home
        }


class GeoRib(models.Model):
    parent = models.ForeignKey('self', related_name='child', null=True)


class GeoPoint(models.Model):
    lat = models.FloatField(max_length=255)
    lon = models.FloatField(max_length=255)
    rib = models.ForeignKey(GeoRib)