# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 20:56
from __future__ import unicode_literals

import common.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CliqueGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CliqueUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_id', models.TextField()),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='cliquegroup',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='Slack.CliqueUser'),
        ),
        migrations.AddField(
            model_name='cliquegroup',
            name='members',
            field=models.ManyToManyField(to='Slack.CliqueUser'),
        ),
    ]
