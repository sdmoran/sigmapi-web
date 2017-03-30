# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyList', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partyguest',
            options={'verbose_name': 'Party Guest', 'verbose_name_plural': 'Party Guests', 'permissions': (('can_destroy_any_party_guest', 'Can Remove Any Party Guest'),)},
        ),
    ]
