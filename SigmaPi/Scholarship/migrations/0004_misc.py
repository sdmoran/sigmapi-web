# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarship', '0003_auto_20160403_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicresource',
            name='resource_pdf',
            field=models.FileField(upload_to='protected/scholarship/resources'),
        ),
        migrations.AlterField(
            model_name='academicresource',
            name='term',
            field=models.CharField(choices=[('A', 'A Term'), ('B', 'B Term'), ('C', 'C Term'), ('D', 'D Term'), ('E', 'E Term')], max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='libraryitem',
            name='course',
            field=models.CharField(default='', max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='libraryitem',
            name='item_pdf',
            field=models.FileField(upload_to='protected/scholarship/library'),
        ),
    ]
