# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0008_auto_20150308_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.FloatField(default=8, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='lon',
            field=models.FloatField(default=9, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venue',
            name='company',
            field=models.ForeignKey(related_name='venue', to='pizza_delivery_app.Company'),
            preserve_default=True,
        ),
    ]
