# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='aboutme',
            field=models.TextField(default=b' ', max_length=1000),
        ),
    ]
