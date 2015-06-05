# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0010_auto_20150529_0647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fbaccount',
            old_name='access_token',
            new_name='facebook_token',
        ),
    ]
