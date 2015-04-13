from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name='child', null=True)
    description = models.CharField(max_length=255)
    image_url = models.URLField(max_length=1000, null=True)

    def get_first_category(self):
        category = self
        while category.parent:
            category = category.parent
        return category

    def get_venues(self):
        from venue import Venue
        return Venue.objects.filter(first_category=self.get_first_category())

    def delete_category(self):
        for product in self.product_category.all():
            product.full_delete()
        for child in self.child.all():
            child.delete_category()
        self.delete()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image_url
        }


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product_category')
    min_price = models.IntegerField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_url = models.URLField(max_length=1000, null=True)

    def save_in_venues(self, creator_venue):
        from venue import VenueProduct

        for venue in self.category.get_venues():
            if venue == creator_venue:
                VenueProduct(venue=venue, product=self, price=self.min_price).save()
            else:
                VenueProduct(venue=venue, product=self, price=self.min_price, status=VenueProduct.UNAVAIL).save()

    def full_delete(self):
        from venue import VenueProduct
        VenueProduct.objects.filter(product=self).delete()
        self.delete()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url
        }


class SingleModifier(models.Model):
    name = models.CharField(max_length=255)
    min_price = models.IntegerField(max_length=255, default=0)
    image_url = models.URLField(max_length=1000, null=True)

    def save_in_venues(self, creator_venue):
        for venue in creator_venue.first_category.get_venues():
            venue.single_modifiers.add(self)
            venue.save()

    def full_delete(self):  # TODO: fill it
        pass

    def dict(self):
        return {
            'name': self.name,
            'image_url': self.image_url
        }


class GroupModifier(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=1000, null=True)

    def save_in_venues(self, creator_venue):
        for venue in creator_venue.first_category.get_venues():
            venue.group_modifiers.add(self)
            venue.save()


class GroupModifierItem(models.Model):
    name = models.CharField(max_length=255)
    min_price = models.IntegerField(max_length=255, default=0)
    image_url = models.URLField(max_length=1000, null=True)
    group_modifier = models.ForeignKey(GroupModifier, related_name='group_modifier_item')


class ModifierBinding(models.Model):
    product = models.ForeignKey(Product)
    modifier = models.ForeignKey(SingleModifier)

    def save_in_venues(self):  # TODO: fill this code!
        pass

    def dict(self):
        return self.modifier.dict()


class GroupModifierBinding(models.Model):
    product = models.ForeignKey(Product)
    modifier = models.ForeignKey(GroupModifier)

    def save_in_venues(self):  # TODO: fill this code!
        pass