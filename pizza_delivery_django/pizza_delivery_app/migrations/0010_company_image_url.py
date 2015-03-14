# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0009_auto_20150308_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='image_url',
            field=models.URLField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
