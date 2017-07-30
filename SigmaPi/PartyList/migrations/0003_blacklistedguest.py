# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyList', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedGuest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('details', models.CharField(max_length=200)),
            ],
            options={
                'permissions': (('manage_blacklist', 'Can manage the blacklist'),)
            },
        ),
    ]
