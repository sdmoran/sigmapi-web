# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mafiagame',
            old_name='finished',
            new_name='is_finished',
        ),
    ]
