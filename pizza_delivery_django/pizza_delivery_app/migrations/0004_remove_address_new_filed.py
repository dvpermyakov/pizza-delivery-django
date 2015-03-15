# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0003_address_new_filed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='new_filed',
        ),
    ]
