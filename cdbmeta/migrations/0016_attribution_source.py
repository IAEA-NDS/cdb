# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-23 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refs', '0001_initial'),
        ('cdbmeta', '0015_auto_20190522_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribution',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='refs.Ref'),
        ),
    ]
