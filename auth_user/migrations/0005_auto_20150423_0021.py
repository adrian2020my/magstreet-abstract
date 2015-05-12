# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_auto_20150423_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='fb_token',
            new_name='facebook_token',
        ),
    ]
