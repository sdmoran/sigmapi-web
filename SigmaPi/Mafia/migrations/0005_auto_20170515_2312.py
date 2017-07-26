# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mafia', '0004_auto_20170512_1239'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('night_number', models.PositiveSmallIntegerField()),
                ('action_type', models.CharField(default=b'NA', max_length=2, choices=[(b'Am', b'Ambush'), (b'BV', b'Bulletproof Vest'), (b'Co', b'Control'), (b'Co', b'Corrupt'), (b'De', b'Defend'), (b'Di', b'Dispose'), (b'Do', b'Douse'), (b'Fo', b'Follow'), (b'FI', b'Forgetful Investigate'), (b'Fr', b'Frame'), (b'Ig', b'Ignite'), (b'II', b'Insane Investigate'), (b'In', b'Investigate'), (b'NA', b'No Action'), (b'OG', b'On Guard'), (b'Pr', b'Protect'), (b'Re', b'Remember'), (b'Re', b'Reveal'), (b'Sa', b'Sabotage'), (b'Sc', b'Scrutinize'), (b'Se', b'Seduce'), (b'Sl', b'Slay'), (b'Sn', b'Snipe'), (b'Sw', b'Switch'), (b'UD', b'Un-Douse'), (b'Wa', b'Watch')])),
            ],
        ),
        migrations.CreateModel(
            name='DayResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_number', models.PositiveSmallIntegerField()),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Unnamed Mafia Game', max_length=50)),
                ('created', models.DateField()),
                ('day_number', models.PositiveSmallIntegerField(default=0)),
                ('time', models.CharField(default=b'U', max_length=1, choices=[(b'A', b'Dawn'), (b'D', b'Day'), (b'U', b'Dusk'), (b'N', b'Night')])),
                ('is_finished', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NightResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('night_number', models.PositiveSmallIntegerField()),
                ('description', models.TextField(default=b'')),
                ('game', models.ForeignKey(to='Mafia.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic '), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Mt', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')])),
                ('old_role', models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic '), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Mt', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')])),
                ('older_role', models.CharField(blank=True, max_length=2, null=True, choices=[(b'RE', b'Amnesiac'), (b'RA', b'Arsonist'), (b'Ma', b'Basic '), (b'Va', b'Basic Villager'), (b'Vg', b'Bodyguard'), (b'Vo', b'Bomb'), (b'VB', b'Bus Driver'), (b'VC', b'Cop'), (b'Ve', b'Detective'), (b'VD', b'Doctor'), (b'VE', b'Escort'), (b'RX', b'Executioner'), (b'VF', b'Forgetful Cop'), (b'MF', b'Framer'), (b'MG', b'Godfather'), (b'MH', b'Hooker'), (b'VI', b'Insane Cop'), (b'MJ', b'Janitor'), (b'RJ', b'Jester'), (b'ML', b'Limo Driver'), (b'Mk', b'Lookout'), (b'RM', b'Mass Murderer'), (b'VM', b'Mayor'), (b'Vl', b'Miller'), (b'Mt', b'Saboteur'), (b'RK', b'Serial Killer'), (b'Mi', b'Sniper'), (b'MS', b'Stalker'), (b'RS', b'Survivor'), (b'VT', b'Tracker'), (b'VV', b'Veteran'), (b'Vi', b'Vigilante'), (b'VW', b'Watcher'), (b'RW', b'Witch'), (b'MY', b'Yakuza')])),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Alive'), (b'K', b'Died at Night'), (b'L', b'Lynched')])),
                ('actions_used_json', models.TextField(default=b'{}')),
                ('doused', models.BooleanField(default=False)),
                ('executioner_target', models.ForeignKey(related_name='executioner_target', to=settings.AUTH_USER_MODEL, null=True)),
                ('game', models.ForeignKey(to='Mafia.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerNightResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('switched_by_json', models.TextField(default=b'[]')),
                ('attempted_seduced', models.BooleanField(default=False)),
                ('framed', models.BooleanField(default=False)),
                ('protected_by_json', models.TextField(default=b'[]')),
                ('defended_by_json', models.TextField(default=b'[]')),
                ('attempted_corrupted', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'S', max_length=1, choices=[(b'A', b'Attacked'), (b'S', b'Safe'), (b'T', b'Terimated')])),
                ('doused', models.BooleanField(default=False)),
                ('un_doused', models.BooleanField(default=False)),
                ('disposed', models.BooleanField(default=False)),
                ('action_effective', models.BooleanField(default=False)),
                ('other_targeted_by_json', models.TextField(default=b'[]')),
                ('report', models.TextField(default=b'')),
                ('action', models.OneToOneField(to='Mafia.Action')),
                ('controlled_to_target', models.ForeignKey(related_name='controlled_to_target', to=settings.AUTH_USER_MODEL, null=True)),
                ('remembered', models.ForeignKey(related_name='remembered', to=settings.AUTH_USER_MODEL, null=True)),
                ('switched_with', models.ForeignKey(related_name='switched_with', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_number', models.PositiveSmallIntegerField()),
                ('vote_type', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Abstain'), (b'L', b'Lynch'), (b'N', b'No Lynch')])),
                ('comment', models.TextField(default=b'')),
                ('vote', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('voter', models.ForeignKey(to='Mafia.Player')),
            ],
        ),
        migrations.RemoveField(
            model_name='mafiaaction',
            name='performer',
        ),
        migrations.RemoveField(
            model_name='mafiaaction',
            name='target0',
        ),
        migrations.RemoveField(
            model_name='mafiaaction',
            name='target1',
        ),
        migrations.RemoveField(
            model_name='mafiadayresult',
            name='game',
        ),
        migrations.RemoveField(
            model_name='mafiadayresult',
            name='lynched',
        ),
        migrations.RemoveField(
            model_name='mafiagame',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='mafianightresult',
            name='game',
        ),
        migrations.RemoveField(
            model_name='mafiaplayer',
            name='executioner_target',
        ),
        migrations.RemoveField(
            model_name='mafiaplayer',
            name='game',
        ),
        migrations.RemoveField(
            model_name='mafiaplayer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mafiaplayernightresult',
            name='action',
        ),
        migrations.RemoveField(
            model_name='mafiaplayernightresult',
            name='controlled_to_target',
        ),
        migrations.RemoveField(
            model_name='mafiaplayernightresult',
            name='remembered',
        ),
        migrations.RemoveField(
            model_name='mafiaplayernightresult',
            name='switched_with',
        ),
        migrations.RemoveField(
            model_name='mafiavote',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='mafiavote',
            name='voter',
        ),
        migrations.DeleteModel(
            name='MafiaAction',
        ),
        migrations.DeleteModel(
            name='MafiaDayResult',
        ),
        migrations.DeleteModel(
            name='MafiaGame',
        ),
        migrations.DeleteModel(
            name='MafiaNightResult',
        ),
        migrations.DeleteModel(
            name='MafiaPlayer',
        ),
        migrations.DeleteModel(
            name='MafiaPlayerNightResult',
        ),
        migrations.DeleteModel(
            name='MafiaVote',
        ),
        migrations.AddField(
            model_name='dayresult',
            name='game',
            field=models.ForeignKey(to='Mafia.Game'),
        ),
        migrations.AddField(
            model_name='dayresult',
            name='lynched',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='performer',
            field=models.ForeignKey(to='Mafia.Player'),
        ),
        migrations.AddField(
            model_name='action',
            name='target0',
            field=models.ForeignKey(related_name='target0', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='target1',
            field=models.ForeignKey(related_name='target1', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]