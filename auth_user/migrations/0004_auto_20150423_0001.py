# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0003_remove_myuser_aboutme'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='fb_token',
            field=models.CharField(default=b' ', max_length=100),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
