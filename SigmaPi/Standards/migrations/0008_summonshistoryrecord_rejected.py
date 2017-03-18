# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0007_auto_20170317_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='summonshistoryrecord',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
