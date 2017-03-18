# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Standards', '0004_auto_20170316_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequest',
            name='requester',
        ),
        migrations.RemoveField(
            model_name='pipointschangerecord',
            name='brother',
        ),
        migrations.RemoveField(
            model_name='pipointschangerecord',
            name='modifier',
        ),
        migrations.RemoveField(
            model_name='pipointsrecord',
            name='brother',
        ),
        migrations.RemoveField(
            model_name='pipointsrequest',
            name='requester',
        ),
        migrations.RemoveField(
            model_name='probation',
            name='giver',
        ),
        migrations.RemoveField(
            model_name='probation',
            name='recipient',
        ),
        migrations.DeleteModel(
            name='JobRequest',
        ),
        migrations.DeleteModel(
            name='PiPointsChangeRecord',
        ),
        migrations.DeleteModel(
            name='PiPointsRecord',
        ),
        migrations.DeleteModel(
            name='PiPointsRequest',
        ),
        migrations.DeleteModel(
            name='Probation',
        ),
    ]
