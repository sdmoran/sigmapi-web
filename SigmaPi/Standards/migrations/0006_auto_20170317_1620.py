# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Standards', '0005_auto_20170316_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bone',
            name='bonee',
        ),
        migrations.RemoveField(
            model_name='bone',
            name='boner',
        ),
        migrations.RemoveField(
            model_name='bonechangerecord',
            name='bone',
        ),
        migrations.RemoveField(
            model_name='bonechangerecord',
            name='modifier',
        ),
        migrations.RemoveField(
            model_name='summonshistoryrecord',
            name='boneID',
        ),
        migrations.RemoveField(
            model_name='summonshistoryrecord',
            name='hasBone',
        ),
        migrations.AddField(
            model_name='summonshistoryrecord',
            name='saved_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
