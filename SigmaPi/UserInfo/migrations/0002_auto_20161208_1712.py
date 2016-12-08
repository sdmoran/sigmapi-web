# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='classYear',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='graduationYear',
            field=models.PositiveIntegerField(default=2020),
        ),
    ]
