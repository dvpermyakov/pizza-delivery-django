# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0003_auto_20150307_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='image_url',
            field=models.URLField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='first_category',
            field=models.OneToOneField(default=123, to='pizza_delivery_app.Category'),
            preserve_default=False,
        ),
    ]
