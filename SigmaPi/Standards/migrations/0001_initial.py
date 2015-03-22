# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.TextField()),
                ('dateReceived', models.DateField()),
                ('expirationDate', models.DateField()),
                ('value', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Bone',
                'verbose_name_plural': 'Bones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BoneChangeRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateChangeMade', models.DateTimeField()),
                ('previousReason', models.TextField()),
                ('newReason', models.TextField()),
                ('previousExpirationDate', models.DateField()),
                ('newExpirationDate', models.DateField()),
                ('bone', models.ForeignKey(to='Standards.Bone')),
            ],
            options={
                'verbose_name': 'Bone Change Record',
                'verbose_name_plural': 'Bone Change Records',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('job', models.TextField(max_length=1, choices=[(b'P', b'Pre/Post Party Job (10)'), (b'F', b'First Shift Party Job (30)'), (b'S', b'Second Shift Party Job (40)'), (b'H', b'House Job (20)'), (b'M', b'Meal Crew (20)')])),
                ('details', models.TextField()),
                ('takingJob', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Job Request',
                'verbose_name_plural': 'Job Requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PiPointsChangeRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateChanged', models.DateTimeField()),
                ('oldValue', models.PositiveIntegerField(default=0)),
                ('newValue', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Pi Points Change Record',
                'verbose_name_plural': 'Pi Points Change Records',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PiPointsRecord',
            fields=[
                ('brother', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('jobsTaken', models.PositiveIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Pi Points Record',
                'verbose_name_plural': 'Pi Points Records',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PiPointsRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField(max_length=1, choices=[(b'P', b'Pre/Post Party Job'), (b'F', b'First Shift Party Job'), (b'S', b'Second Shift Party Job'), (b'H', b'House Job'), (b'M', b'Meal Crew')])),
                ('witness', models.CharField(default=b'None', max_length=100)),
                ('requester', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pi Points Request',
                'verbose_name_plural': 'Pi Points Request',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Probation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateReceived', models.DateField()),
                ('expirationDate', models.DateField()),
                ('giver', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Probation',
                'verbose_name_plural': 'Probations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Summons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.TextField()),
                ('dateSummonsSent', models.DateField()),
                ('approver', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('summonee', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('summoner', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Summons',
                'verbose_name_plural': 'Summonses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SummonsHistoryRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.TextField()),
                ('resultReason', models.TextField()),
                ('date', models.DateField()),
                ('hasBone', models.BooleanField(default=False)),
                ('boneID', models.PositiveIntegerField()),
                ('summonee', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('summoner', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SummonsRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.TextField()),
                ('dateRequestSent', models.DateField()),
                ('summonee', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('summoner', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Summons Request',
                'verbose_name_plural': 'Summons Requests',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pipointschangerecord',
            name='brother',
            field=models.ForeignKey(to='Standards.PiPointsRecord'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pipointschangerecord',
            name='modifier',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='requester',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bonechangerecord',
            name='modifier',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bone',
            name='bonee',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bone',
            name='boner',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
