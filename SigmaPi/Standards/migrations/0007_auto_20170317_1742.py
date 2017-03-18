# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0006_auto_20170317_1620'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bone',
        ),
        migrations.DeleteModel(
            name='BoneChangeRecord',
        ),
    ]
