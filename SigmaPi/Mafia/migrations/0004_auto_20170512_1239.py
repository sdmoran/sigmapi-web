# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0003_auto_20170510_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mafiagame',
            name='name',
            field=models.CharField(default=b'Unnamed Mafia Game', max_length=50),
        ),
    ]
