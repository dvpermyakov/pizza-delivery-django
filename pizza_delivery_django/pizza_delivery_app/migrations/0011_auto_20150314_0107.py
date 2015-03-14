# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_delivery_app', '0010_company_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupModifierBinding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modifier', models.ForeignKey(to='pizza_delivery_app.GroupModifier')),
                ('product', models.ForeignKey(to='pizza_delivery_app.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupModifierItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('min_price', models.IntegerField(default=0, max_length=255)),
                ('image_url', models.URLField(max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModifierBinding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SingleModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('min_price', models.IntegerField(default=0, max_length=255)),
                ('image_url', models.URLField(max_length=255, null=True)),
                ('products', models.ManyToManyField(to='pizza_delivery_app.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VenueGroupModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, max_length=255, choices=[(0, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd'), (1, b'\xd0\x9d\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd')])),
                ('modifier_binding', models.ForeignKey(to='pizza_delivery_app.GroupModifierBinding')),
                ('venue', models.ForeignKey(to='pizza_delivery_app.Venue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VenueGroupModifierItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(max_length=255)),
                ('status', models.IntegerField(default=0, max_length=255, choices=[(0, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd'), (1, b'\xd0\x9d\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd')])),
                ('group_modifier_item', models.ForeignKey(to='pizza_delivery_app.GroupModifierItem')),
                ('venue', models.ForeignKey(to='pizza_delivery_app.Venue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VenueModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(max_length=255)),
                ('status', models.IntegerField(default=0, max_length=255, choices=[(0, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd'), (1, b'\xd0\x9d\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd')])),
                ('modifier_binding', models.ForeignKey(to='pizza_delivery_app.ModifierBinding')),
                ('venue', models.ForeignKey(to='pizza_delivery_app.Venue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='modifierbinding',
            name='modifier',
            field=models.ForeignKey(to='pizza_delivery_app.SingleModifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modifierbinding',
            name='product',
            field=models.ForeignKey(to='pizza_delivery_app.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmodifier',
            name='choices',
            field=models.ForeignKey(related_name='group_modifier', to='pizza_delivery_app.GroupModifierItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmodifier',
            name='products',
            field=models.ManyToManyField(to='pizza_delivery_app.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='venue',
            name='group_modifiers',
            field=models.ManyToManyField(to='pizza_delivery_app.GroupModifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='venue',
            name='single_modifiers',
            field=models.ManyToManyField(to='pizza_delivery_app.SingleModifier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='first_category',
            field=models.ForeignKey(to='pizza_delivery_app.Category'),
            preserve_default=True,
        ),
    ]
