# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0002_auto_20170510_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mafiagame',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.AlterField(
            model_name='mafiaplayer',
            name='old_role',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic Mafia'), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Ma', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')]),
        ),
        migrations.AlterField(
            model_name='mafiaplayer',
            name='older_role',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic Mafia'), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Ma', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')]),
        ),
        migrations.AlterField(
            model_name='mafiaplayer',
            name='role',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic Mafia'), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Ma', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')]),
        ),
    ]
