# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Archives.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bylaws',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('filepath', models.FileField(upload_to=Archives.models.bylaws_path)),
            ],
            options={
                'verbose_name': 'Bylaws',
                'verbose_name_plural': 'Bylaws',
                'permissions': (('access_bylaws', 'Can access bylaws.'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('datePosted', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('filepath', models.FileField(upload_to=Archives.models.guidepath)),
                ('path', models.SlugField(max_length=15)),
            ],
            options={
                'verbose_name': 'Guide',
                'verbose_name_plural': 'Guides',
                'permissions': (('access_guide', 'Can access guides.'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HouseRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('filepath', models.FileField(upload_to=Archives.models.houserules_path)),
            ],
            options={
                'verbose_name': 'House Rules',
                'verbose_name_plural': 'House Rules',
                'permissions': (('access_houserules', 'Can access house rules.'),),
            },
            bases=(models.Model,),
        ),
    ]
