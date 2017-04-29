# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyList', '0002_auto_20170330_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='girl_delta',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='party',
            name='guy_delta',
            field=models.IntegerField(default=0),
        ),
    ]
