# coding: utf-8

from django.db import models
from address import Address
from menu import Category, Product, ModifierBinding, GroupModifierBinding, GroupModifierItem, SingleModifier,\
    GroupModifier
from collections import deque
from company import Company
from pizza_delivery_app.methods import storage_disk


class Venue(models.Model):
    company = models.ForeignKey(Company, related_name='venue')
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    manager_username = models.CharField(max_length=255)
    first_category = models.ForeignKey(Category)
    single_modifiers = models.ManyToManyField(SingleModifier)
    group_modifiers = models.ManyToManyField(GroupModifier)

    @classmethod
    def create(cls, company, address, name, description, manager_username, first_category=None):
        if first_category:
            venue = cls(company=company, address=address, name=name, description=description,
                        first_category=first_category, manager_username=manager_username)
            venue.save()
            for product in venue.get_products_from_menu(venue_product=False):
                VenueProduct(venue=venue, product=product, price=product.min_price).save()
        else:
            first_category = Category(name='Меню', description='Корень меню')
            first_category.save()
            venue = cls(company=company, address=address, name=name, description=description,
                        first_category=first_category, manager_username=manager_username)
            venue.save()
        storage_disk.create_venue_folder(venue)
        return venue

    def get_products_from_menu(self, venue_product=True):
        def get_products(category):
            if venue_product:
                return [product.venue_product.get(venue=self) for product in category.product_category.all()]
            else:
                return category.product_category.all()

        def get_categories(category):
            return category.child.all()

        products = []
        queue = deque([self.first_category])
        while len(queue):
            category = queue.popleft()
            products.extend(get_products(category))
            queue.extend(get_categories(category))
        return products

    def get_menu(self, venue_product=True):
        def get_products(category):
            if venue_product:
                return [product.venue_product.get(venue=self) for product in category.product_category.all()]
            else:
                return category.product_category.all()

        def get_category_info(category):
            return {
                'products': get_products(category),
                'category': category,
                'children': [get_category_info(child_category) for child_category in category.child.all()]
            }

        return get_category_info(self.first_category)


class VenueProduct(models.Model):
    AVAIL = 0
    UNAVAIL = 1

    STATUS_CHOICES = (
        (AVAIL, 'Доступен'),
        (UNAVAIL, 'Не доступен')
    )

    venue = models.ForeignKey(Venue)
    product = models.ForeignKey(Product, related_name='venue_product')
    price = models.IntegerField(max_length=255)
    status = models.IntegerField(max_length=255, choices=STATUS_CHOICES, default=AVAIL)

    def change_status(self):
        self.status += 1
        self.status %= 2
        self.save()

    def dict(self):
        return self.product.dict().update({
            'price': self.price,
            'status': self.status
        })


class VenueModifier(models.Model):
    AVAIL = 0
    UNAVAIL = 1

    STATUS_CHOICES = (
        (AVAIL, 'Доступен'),
        (UNAVAIL, 'Не доступен')
    )

    venue = models.ForeignKey(Venue)
    modifier_binding = models.ForeignKey(ModifierBinding)
    price = models.IntegerField(max_length=255)
    status = models.IntegerField(max_length=255, choices=STATUS_CHOICES, default=AVAIL)


class VenueGroupModifier(models.Model):
    AVAIL = 0
    UNAVAIL = 1

    STATUS_CHOICES = (
        (AVAIL, 'Доступен'),
        (UNAVAIL, 'Не доступен')
    )

    venue = models.ForeignKey(Venue)
    modifier_binding = models.ForeignKey(GroupModifierBinding)
    status = models.IntegerField(max_length=255, choices=STATUS_CHOICES, default=AVAIL)

    def get_items(self):
        return [VenueGroupModifierItem.objects.filter(venue=self.venue,
                                                      group_modifier_item__in=self.group_modifier.modifier.choices)]


class VenueGroupModifierItem(models.Model):
    AVAIL = 0
    UNAVAIL = 1

    STATUS_CHOICES = (
        (AVAIL, 'Доступен'),
        (UNAVAIL, 'Не доступен')
    )

    venue = models.ForeignKey(Venue)
    group_modifier_item = models.ForeignKey(GroupModifierItem)
    price = models.IntegerField(max_length=255)
    status = models.IntegerField(max_length=255, choices=STATUS_CHOICES, default=AVAIL)