# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0009_auto_20150511_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='cover_img',
            field=models.CharField(default=b' ', max_length=250),
        ),
        migrations.AddField(
            model_name='myuser',
            name='profile_img',
            field=models.CharField(default=b' ', max_length=250),
        ),
    ]
