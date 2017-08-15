# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summonsrequest',
            name='outcomes',
            field=models.TextField(blank=True),
        ),
        migrations.RenameField(
            model_name='summonsrequest',
            old_name='reason',
            new_name='special_circumstance'
        ),
        migrations.AddField(
            model_name='summonsrequest',
            name='spokeWith',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='summonsrequest',
            name='standards_action',
            field=models.TextField(blank=True),
        ),
    ]
