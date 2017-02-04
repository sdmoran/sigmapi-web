# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0002_auto_20161208_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pledgeclass',
            options={'ordering': ['dateInitiated'], 'verbose_name': 'Pledge Class', 'verbose_name_plural': 'Pledge Classes'},
        ),
    ]
