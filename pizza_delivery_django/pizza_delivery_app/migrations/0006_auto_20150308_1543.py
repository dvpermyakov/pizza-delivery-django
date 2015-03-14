# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0005_address_venue'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenueProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(max_length=255)),
                ('status', models.IntegerField(default=0, max_length=255, choices=[(0, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd'), (1, b'\xd0\x9d\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd')])),
                ('product', models.ForeignKey(to='pizza_delivery_app.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='min_price',
        ),
    ]
