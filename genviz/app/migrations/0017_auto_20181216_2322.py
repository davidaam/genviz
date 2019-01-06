# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-16 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20181216_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associationrules',
            name='graph',
            field=models.FileField(default=None, null=True, upload_to='genviz/static/charts'),
        ),
        migrations.AlterField(
            model_name='associationrules',
            name='heat_map',
            field=models.FileField(default=None, null=True, upload_to='genviz/static/charts'),
        ),
        migrations.AlterField(
            model_name='associationrules',
            name='histogram',
            field=models.FileField(default=None, null=True, upload_to='genviz/static/charts'),
        ),
        migrations.AlterField(
            model_name='associationrules',
            name='scatter',
            field=models.FileField(default=None, null=True, upload_to='genviz/static/charts'),
        ),
    ]