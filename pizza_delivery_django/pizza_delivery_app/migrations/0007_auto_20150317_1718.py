# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0006_auto_20150317_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmodifier',
            name='choices',
        ),
        migrations.AddField(
            model_name='groupmodifieritem',
            name='group_modifier',
            field=models.ForeignKey(related_name='group_modifier_item', default=1, to='pizza_delivery_app.GroupModifier'),
            preserve_default=False,
        ),
    ]
