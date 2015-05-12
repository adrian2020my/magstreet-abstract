# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0008_fbaccount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fbaccount',
            old_name='user_id',
            new_name='user',
        ),
    ]
