# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0002_auto_20150307_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='chief',
        ),
        migrations.AddField(
            model_name='company',
            name='chief_username',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
    ]
