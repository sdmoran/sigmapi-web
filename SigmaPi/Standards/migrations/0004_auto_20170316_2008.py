# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0003_auto_20160930_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summonshistoryrecord',
            options={'verbose_name': 'Summons History Record', 'verbose_name_plural': 'Summons History Records'},
        ),
    ]
