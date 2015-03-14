# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0006_auto_20150308_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='venueproduct',
            name='venue',
            field=models.ForeignKey(default=123, to='pizza_delivery_app.Venue'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venueproduct',
            name='product',
            field=models.ForeignKey(related_name='venue_product', to='pizza_delivery_app.Product'),
            preserve_default=True,
        ),
    ]
