from django.db import models


class Address(models.Model):
    lat = models.FloatField(max_length=255)
    lon = models.FloatField(max_length=255)

    timezone_offset = models.IntegerField(null=True)
    timezone_id = models.CharField(max_length=255, null=True)
    timezone_name = models.CharField(max_length=255, null=True)

    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    home = models.CharField(max_length=255)

    def to_str(self):
        if self.city and self.street and self.home:
            return '%s, %s, %s' % (self.city, self.street, self.home)
        else:
            return ''

    def dict(self):
        return {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
            'city': self.city,
            'street': self.street,
            'home': self.home
        }


class GeoRib(models.Model):
    parent = models.ForeignKey('self', related_name='child', null=True)

    def get_ribs(self):
        rib = self
        result = []
        while rib not in result:
            result.append(rib)
            if rib.child.all():
                rib = rib.child.all()[0]
        return result

    def get_polygon(self):
        points = []
        for rib in self.get_ribs():
            points.append(GeoPoint.objects.filter(rib=rib)[0])
        return points

    def get_points(self):
        return GeoPoint.objects.filter(rib=self)


class GeoPoint(models.Model):
    lat = models.FloatField(max_length=255)
    lon = models.FloatField(max_length=255)
    rib = models.ForeignKey(GeoRib)

    @staticmethod
    def square(a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    @property
    def x(self):
        return self.lat

    @property
    def y(self):
        return self.lon