# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0005_address_new_filed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='new_filed',
        ),
        migrations.AlterField(
            model_name='groupmodifier',
            name='choices',
            field=models.ForeignKey(related_name='group_modifier', to='pizza_delivery_app.GroupModifierItem', null=True),
            preserve_default=True,
        ),
    ]
