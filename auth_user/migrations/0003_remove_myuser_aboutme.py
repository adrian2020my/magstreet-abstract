# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0002_myuser_aboutme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='aboutme',
        ),
    ]
