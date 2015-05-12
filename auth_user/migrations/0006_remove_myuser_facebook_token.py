# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0005_auto_20150423_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='facebook_token',
        ),
    ]
