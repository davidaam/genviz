# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-21 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180709_0704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_id', models.CharField(default=None, max_length=15)),
                ('individual_id', models.CharField(default=None, max_length=15)),
                ('paternal_id', models.CharField(default='0', max_length=15)),
                ('maternal_id', models.CharField(default='0', max_length=15)),
                ('gender', models.CharField(default='0', max_length=1)),
                ('population', models.CharField(default=None, max_length=5)),
                ('relationship', models.CharField(default=None, max_length=20)),
                ('siblings', models.CharField(default=None, max_length=100)),
                ('second_order', models.CharField(default=None, max_length=100)),
                ('third_order', models.CharField(default=None, max_length=100)),
                ('comments', models.CharField(default=None, max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='variationlocation',
            name='hgvs',
        ),
    ]