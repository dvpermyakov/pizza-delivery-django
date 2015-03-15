# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0004_remove_address_new_filed'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='new_filed',
            field=models.CharField(default=None, max_length=10, null=True),
            preserve_default=True,
        ),
    ]
