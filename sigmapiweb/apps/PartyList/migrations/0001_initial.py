# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from .. import models as mymodels


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('birthDate', models.DateField(auto_now=True)),
                ('gender', models.CharField(max_length=100)),
                ('cardID', models.CharField(max_length=100, blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Guest',
                'verbose_name_plural': 'Guests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('guycount', models.IntegerField(default=0)),
                ('girlcount', models.IntegerField(default=0)),
                ('jobs', models.FileField(null=True, upload_to=mymodels.partyjobspath, blank=True)),
            ],
            options={
                'verbose_name': 'Party',
                'verbose_name_plural': 'Parties',
                'permissions': (('manage_parties', 'Can manage Parties'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartyGuest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('signedIn', models.BooleanField(default=False)),
                ('everSignedIn', models.BooleanField(default=False)),
                ('timeFirstSignedIn', models.DateTimeField(auto_now_add=True)),
                ('addedBy', models.ForeignKey(related_name='added_by', default=1, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('guest', models.ForeignKey(related_name='guest', default=1, to='PartyList.Guest', on_delete=models.CASCADE)),
                ('party', models.ForeignKey(related_name='party_for_guest', default=1, to='PartyList.Party', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Party Guest',
                'verbose_name_plural': 'Party Guests',
            },
            bases=(models.Model,),
        ),
    ]
