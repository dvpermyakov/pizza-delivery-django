from django.contrib.auth.models import Permission
from pizza_delivery_app.models import Category, Product, OrderProduct
from pizza_delivery_app.models.venue import Venue
from pizza_delivery_app.models.menu import SingleModifier, GroupModifier
from django.contrib.contenttypes.models import ContentType

category_ct = ContentType.objects.get_for_model(Category)
product_ct = ContentType.objects.get_for_model(Product)
single_modifier_ct = ContentType.objects.get_for_model(SingleModifier)
group_modifier_ct = ContentType.objects.get_for_model(GroupModifier)
venue_ct = ContentType.objects.get_for_model(Venue)
order_product_ct = ContentType.objects.get_for_model(OrderProduct)

MENU_READ_PERMISSIONS = [
    Permission.objects.get_or_create(codename='read_categories', name='Can read categories', content_type=category_ct)[0],
    Permission.objects.get_or_create(codename='read_products', name='Can read products', content_type=product_ct)[0],
    Permission.objects.get_or_create(codename='read_single_modifiers', name='Can read single modifiers',
                                     content_type=single_modifier_ct)[0],
    Permission.objects.get_or_create(codename='read_group_modifiers', name='Can read group modifiers',
                                     content_type=group_modifier_ct)[0],
]

MENU_CHANGE_PERMISSIONS = [
    Permission.objects.get_or_create(codename='create_categories', name='Can create categories', content_type=category_ct)[0],
    Permission.objects.get_or_create(codename='update_categories', name='Can update categories', content_type=category_ct)[0],
    Permission.objects.get_or_create(codename='delete_categories', name='Can delete categories', content_type=category_ct)[0],
    Permission.objects.get_or_create(codename='create_products', name='Can create products', content_type=product_ct)[0],
    Permission.objects.get_or_create(codename='update_products', name='Can update products', content_type=product_ct)[0],
    Permission.objects.get_or_create(codename='delete_products', name='Can delete products', content_type=product_ct)[0],
    Permission.objects.get_or_create(codename='create_single_modifiers', name='Can create single modifiers',
                                     content_type=single_modifier_ct)[0],
    Permission.objects.get_or_create(codename='update_single_modifiers', name='Can update single modifiers',
                                     content_type=single_modifier_ct)[0],
    Permission.objects.get_or_create(codename='delete_single_modifiers', name='Can read single modifiers',
                                     content_type=single_modifier_ct)[0],
    Permission.objects.get_or_create(codename='create_group_modifiers', name='Can create group modifiers',
                                     content_type=group_modifier_ct)[0],
    Permission.objects.get_or_create(codename='update_group_modifiers', name='Can update group modifiers',
                                     content_type=group_modifier_ct)[0],
    Permission.objects.get_or_create(codename='delete_group_modifiers', name='Can delete group modifiers',
                                     content_type=group_modifier_ct)[0],
]

VENUE_CRUD_PERMISSIONS = [
    Permission.objects.get_or_create(codename='crud_venues', name='Can crud venue', content_type=venue_ct)[0],
]

COOK_PERMISSIONS = [
    Permission.objects.get_or_create(codename='cook', name='Can cook products', content_type=order_product_ct)[0],
]