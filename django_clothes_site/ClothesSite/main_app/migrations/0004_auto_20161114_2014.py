# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-14 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20161111_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes_item',
            name='image',
            field=models.ImageField(default='media/default.png', upload_to='media/clothes_images'),
        ),
    ]
