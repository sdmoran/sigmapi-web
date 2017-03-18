# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import UserInfo.models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0003_auto_20170204_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.FileField(null=True, upload_to=UserInfo.models.filepath, blank=True),
        ),
    ]
