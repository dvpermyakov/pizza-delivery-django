# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0004_auto_20150308_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('home', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('address', models.ForeignKey(to='pizza_delivery_app.Address')),
                ('company', models.ForeignKey(to='pizza_delivery_app.Company')),
                ('first_category', models.OneToOneField(to='pizza_delivery_app.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
