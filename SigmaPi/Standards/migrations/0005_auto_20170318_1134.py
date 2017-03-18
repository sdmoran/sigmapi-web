# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Standards', '0004_auto_20170316_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bone',
            name='bonee',
        ),
        migrations.RemoveField(
            model_name='bone',
            name='boner',
        ),
        migrations.RemoveField(
            model_name='bonechangerecord',
            name='bone',
        ),
        migrations.RemoveField(
            model_name='bonechangerecord',
            name='modifier',
        ),
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
        migrations.RemoveField(
            model_name='summonshistoryrecord',
            name='boneID',
        ),
        migrations.RemoveField(
            model_name='summonshistoryrecord',
            name='hasBone',
        ),
        migrations.AddField(
            model_name='summonshistoryrecord',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='summonshistoryrecord',
            name='saved_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='Bone',
        ),
        migrations.DeleteModel(
            name='BoneChangeRecord',
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
