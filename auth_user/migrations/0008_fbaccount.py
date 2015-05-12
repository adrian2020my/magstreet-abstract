# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import auth_user.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0007_auto_20150507_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.TextField(verbose_name="Facebook User 's Access Token")),
                ('uid', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('extra_data', auth_user.fields.JSONField(default=b'{}', verbose_name='extra data')),
                ('expires_at', models.DateTimeField(null=True, verbose_name='expires at', blank=True)),
                ('user_id', models.OneToOneField(related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
