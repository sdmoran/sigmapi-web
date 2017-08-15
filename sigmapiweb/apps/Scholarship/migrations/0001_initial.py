# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from .. import models as mymodels
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_name', models.CharField(max_length=1000)),
                ('course_number', models.CharField(max_length=100)),
                ('professor_name', models.CharField(max_length=100)),
                ('resource_pdf', models.FileField(upload_to=b'protected/scholarship/resources')),
                ('approved', models.BooleanField(default=False)),
                ('year', models.IntegerField(blank=True)),
                ('term', models.CharField(blank=True, max_length=1, choices=[(b'A', b'A Term'), (b'B', b'B Term'), (b'C', b'C Term'), (b'D', b'D Term'), (b'E', b'E Term')])),
                ('submittedBy', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LibraryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('isbn_number', models.CharField(max_length=100)),
                ('edition', models.CharField(max_length=100)),
                ('item_pdf', models.FileField(upload_to=b'protected/scholarship/library')),
                ('approved', models.BooleanField(default=False)),
                ('submittedBy', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyHoursRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_hours', models.IntegerField(validators=[mymodels.validate_number])),
                ('date', models.DateField(validators=[mymodels.validate_date])),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrackedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_hours', models.IntegerField(validators=[mymodels.validate_number])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'permissions': (('scholarship_head', 'Can modify study hours.'),),
            },
            bases=(models.Model,),
        ),
    ]
