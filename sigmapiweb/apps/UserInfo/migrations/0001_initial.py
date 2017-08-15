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
            name='PledgeClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Lambda', max_length=100)),
                ('dateInitiated', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'Pledge Class',
                'verbose_name_plural': 'Pledge Classes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.FileField(null=True, upload_to=mymodels.filepath)),
                ('phoneNumber', models.CharField(default=b'', max_length=100, blank=True)),
                ('graduationYear', models.PositiveIntegerField(default=2015)),
                ('classYear', models.CharField(default=b'Lambda', max_length=20, blank=True)),
                ('major', models.CharField(max_length=100, blank=True)),
                ('hometown', models.CharField(max_length=100, blank=True)),
                ('activities', models.TextField(blank=True)),
                ('interests', models.TextField(blank=True)),
                ('favoriteMemory', models.TextField(blank=True)),
                ('bigBrother', models.ForeignKey(related_name='big_brother', default=1, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('pledgeClass', models.ForeignKey(to='UserInfo.PledgeClass', on_delete=models.CASCADE)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'User Info',
                'verbose_name_plural': 'User Info',
                'permissions': (('manage_users', 'Can manage users.'),),
            },
            bases=(models.Model,),
        ),
    ]
