# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(max_length=255)),
                ('lon', models.FloatField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('home', models.CharField(max_length=255)),
                ('just_new_field', models.IntegerField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=1000, null=True)),
                ('parent', models.ForeignKey(related_name='child', to='pizza_delivery_app.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('chief_username', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=1000, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(max_length=255)),
                ('lon', models.FloatField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoRib',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent', models.ForeignKey(related_name='child', to='pizza_delivery_app.GeoRib', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=1000, null=True)),
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
                ('image_url', models.URLField(max_length=1000, null=True)),
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
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_price', models.IntegerField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=1000, null=True)),
                ('category', models.ForeignKey(related_name='product_category', to='pizza_delivery_app.Category')),
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
                ('image_url', models.URLField(max_length=1000, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('manager_username', models.CharField(max_length=255)),
                ('address', models.ForeignKey(to='pizza_delivery_app.Address')),
                ('company', models.ForeignKey(related_name='venue', to='pizza_delivery_app.Company')),
                ('first_category', models.ForeignKey(to='pizza_delivery_app.Category')),
                ('first_rib', models.ForeignKey(to='pizza_delivery_app.GeoRib', null=True)),
                ('group_modifiers', models.ManyToManyField(to='pizza_delivery_app.GroupModifier')),
                ('single_modifiers', models.ManyToManyField(to='pizza_delivery_app.SingleModifier')),
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
        migrations.CreateModel(
            name='VenueProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(max_length=255)),
                ('status', models.IntegerField(default=0, max_length=255, choices=[(0, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd'), (1, b'\xd0\x9d\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb5\xd0\xbd')])),
                ('product', models.ForeignKey(related_name='venue_product', to='pizza_delivery_app.Product')),
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
            model_name='groupmodifierbinding',
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
            model_name='geopoint',
            name='rib',
            field=models.ForeignKey(to='pizza_delivery_app.GeoRib'),
            preserve_default=True,
        ),
    ]
