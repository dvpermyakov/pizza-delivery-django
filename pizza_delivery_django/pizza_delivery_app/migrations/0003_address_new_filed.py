# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0002_remove_address_just_new_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='new_filed',
            field=models.CharField(default=b'123', max_length=10),
            preserve_default=True,
        ),
    ]
