# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0005_misc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='pledgeClass',
            field=models.ForeignKey(default=1, to='UserInfo.PledgeClass', on_delete=models.CASCADE),
        ),
    ]
