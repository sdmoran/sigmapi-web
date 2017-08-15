# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from .. import models as mymodels


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0003_auto_20170204_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.FileField(null=True, upload_to=mymodels.filepath, blank=True),
        ),
    ]
