# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-04 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthuser',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]