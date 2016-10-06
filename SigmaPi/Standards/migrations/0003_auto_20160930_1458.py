# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0002_auto_20160926_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='summons',
            name='outcomes',
            field=models.TextField(blank=True),
        ),
        migrations.RenameField(
            model_name='summons',
            old_name='reason',
            new_name='special_circumstance'
        ),
        migrations.AddField(
            model_name='summons',
            name='spokeWith',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='summons',
            name='standards_action',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='summonsrequest',
            name='special_circumstance',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='summons',
            name='special_circumstance',
            field=models.TextField(blank=True),
        )
    ]
