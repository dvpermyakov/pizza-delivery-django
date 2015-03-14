# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0007_auto_20150308_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='first_category',
        ),
        migrations.AddField(
            model_name='venue',
            name='manager_username',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
    ]
