# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('promoted', models.BooleanField(default=False)),
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'permissions': (('promote_link', 'Can promote links.'), ('access_link', 'Can access links.')),
            },
            bases=(models.Model,),
        ),
    ]
