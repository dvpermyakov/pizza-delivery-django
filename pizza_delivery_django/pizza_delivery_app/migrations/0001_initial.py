# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(related_name='child', to='pizza_delivery_app.Category', null=True)),
            ],
            options={
                'permissions': (('create_category', 'Can create categories'), ('read_category', 'Can read categories'), ('update_category', 'Can update categories'), ('delete_category', 'Can delete categories')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('chief', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('first_category', models.OneToOneField(null=True, to='pizza_delivery_app.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField(max_length=255)),
                ('image_url', models.URLField(max_length=255, null=True)),
                ('category', models.ForeignKey(related_name='product_category', to='pizza_delivery_app.Category')),
            ],
            options={
                'permissions': (('create_product', 'Can create products'), ('read_product', 'Can read products'), ('update_product', 'Can update products'), ('delete_product', 'Can delete products')),
            },
            bases=(models.Model,),
        ),
    ]
