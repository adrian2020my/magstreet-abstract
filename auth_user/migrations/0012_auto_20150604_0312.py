# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0011_auto_20150531_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='fb_uid',
            field=models.CharField(default=b' ', max_length=250),
        ),
        migrations.AlterField(
            model_name='fbaccount',
            name='expires_at',
            field=models.DateTimeField(null=True, verbose_name='expires at'),
        ),
    ]
