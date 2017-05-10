
from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict
import json

class ChoiceEnumeration(object):

    def __init__(self, code, name):
        self.code = code
        self.name = name

    @classmethod
    def get_instances(cls):
        return [
            getattr(cls, attr) for attr in dir(cls)
            if getattr(cls, attr).__class__ is cls
        ]

    @classmethod
    def get_instance(cls, code):
        for inst in cls.get_instances():
            if inst.code == code:
                return inst
        else:
            return None

    @classmethod
    def get_instance_from_name(cls, name):
        for inst in cls.get_instances():
            if inst.name == name:
                return inst
        else:
            return None

    @classmethod
    def get_choice_tuples(cls):
        return [
            (inst.code, inst.name)
            for inst in cls.get_instances()
        ]

class MafiaGameStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

class MafiaGameTime(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaGameTime.DAWN = MafiaGameTime('A', 'Dawn')
MafiaGameTime.DAY = MafiaGameTime('D', 'Day')
MafiaGameTime.DUSK = MafiaGameTime('U', 'Dusk')
MafiaGameTime.NIGHT = MafiaGameTime('N', 'Night')

class MafiaGame(models.Model):
    name = models.CharField(max_length=50, default='Untitled Mafia Game')
    created = models.DateField()
    creator = models.ForeignKey(User)
    day_number = models.PositiveSmallIntegerField(default=0)
    time = models.CharField(
        max_length=MafiaGameTime.CODE_LENGTH,
        choices=MafiaGameTime.get_choice_tuples(),
        default=MafiaGameTime.DUSK.code
    )
    is_finished = models.BooleanField(default=False)

    @property
    def is_inviting(self):
        return self.day_number == 0

    @property
    def status_string(self):
        if self.is_finished:
            return 'Complete'
        elif self.is_inviting:
            return 'Inviting'
        else:
            time_name = MafiaGameTime.get_instance(self.time).name
            return name + ' ' + `self.day_number`
        
class MafiaFaction(object):
    VILLAGE = 'V'
    MAFIA = 'M'
    ROGUE = 'R'

class MafiaActionType(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, targets_can_be_self,
                 apparent_name=None, targets_dead=False,
                 can_target_self=True, is_direct_offense=False,
                 is_lethal=False, is_covert=False):
        super(MafiaActionType, self).__init__(code, name)
        self.targets_can_be_self = targets_can_be_self
        self.apparent_name = apparent_name or name
        self.targets_can_be_self = targets_can_be_self
        self.can_target_self = can_target_self
        self.is_direct_offense = is_direct_offense
        self.is_covert = True

    @property
    def num_targets(self):
        return len(targets_can_be_self)

MafiaActionType.NO_ACTION = MafiaActionType('NA', 'No Action', [])
MafiaActionType.CONTROL = MafiaActionType('Co', 'Control', [False, True])
MafiaActionType.ON_GUARD = MafiaActionType('OG', 'On Guard', [], is_lethal=True)
MafiaActionType.SEDUCE = MafiaActionType('Se', 'Seduce', [False])
MafiaActionType.SWITCH = MafiaActionType('Sw', 'Switch', [True, True])
MafiaActionType.FRAME = MafiaActionType('Fr', 'Frame', 1)
MafiaActionType.INVESTIGATE = MafiaActionType('In', 'Investigate', [False])
MafiaActionType.INSANE_INVESTIGATE = MafiaActionType('II', 'Insane Investigate', [False], apparent_name='Investigate')
MafiaActionType.FORGETFUL_INVESTIGATE = MafiaActionType('FI', 'Forgetful Investigate', [True])
MafiaActionType.SCRUTINIZE = MafiaActionType('Sc', 'Scrutinize', 1)
MafiaActionType.PROTECT = MafiaActionType('Pr', 'Protect', [False])
MafiaActionType.DEFEND = MafiaActionType('De', 'Defend', 1, [False], is_lethal=True)
MafiaActionType.BULLETPROOF_VEST = MafiaActionType('BV', 'Bulletproof Vest', [])
MafiaActionType.CORRUPT = MafiaActionType('Co', 'Corrupt', [False], is_direct_offense=True)
MafiaActionType.SLAY = MafiaActionType('Sl', 'Slay', [True], is_direct_offense=True, is_lethal=True)
MafiaActionType.AMBUSH = MafiaActionType('Am', 'Ambush', [True], is_lethal=True)
MafiaActionType.SNIPE = MafiaActionType('Sn', 'Snipe', [True], is_lethal=True, is_covert=True)
MafiaActionType.IGNITE = MafiaActionType('Ig', 'Ignite', [], is_lethal=True)
MafiaActionType.SABOTAGE = MafiaActionType('Sa', 'Sabotage', [True], is_lethal=True)
MafiaActionType.DOUSE = MafiaActionType('Do', 'Douse', [True])
MafiaActionType.UN_DOUSE = MafiaActionType('UD', 'Un-Douse', [True])
MafiaActionType.DISPOSE = MafiaActionType('Di', 'Dispose', [True])
MafiaActionType.REVEAL = MafiaActionType('Re', 'Reveal', [])
MafiaActionType.FOLLOW = MafiaActionType('Fo', 'Follow', [True])
MafiaActionType.WATCH = MafiaActionType('Wa', 'Watch', [True])
MafiaActionType.REMEMBER = MafiaActionType('Re', 'Remember', [False], targets_dead=True)

class MafiaApparentGuilt(ChoiceEnumeration):
    FACTION_BASED = 0
    INNOCENT = 1
    GUILTY = 2

class MafiaRole(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, faction, action_types_and_uses, apparent_name=None,
                 night_immune=False, immune_to_seduction=False,
                 hidden_to_mafia=False, apparent_guilt=MafiaApparentGuilt.FACTION_BASED,
                 min_in_game=0, max_in_game=float('inf')):
        super(MafiaRole, self).__init__(code, name)

        self.faction = faction
        self.action_types_and_uses = action_types_and_uses
        self.apparent_name = apparent_name or name
        self.night_immune = night_immune
        self.immune_to_seduction = immune_to_seduction

        if self.faction != MafiaFaction.MAFIA and hidden_to_mafia:
            raise ValueError('MafiaRole: faction!=mafia but hidden_to_mafia==True')
        self.hidden_to_mafia = hidden_to_mafia

        self.apparent_guilt = apparent_guilt

        if min_in_game > max_in_game:
            raise ValueError('MafiaRole: min_in_game > max_in_game')
        self.min_in_game = min_in_game
        self.max_in_game = max_in_game

MAFIA_UNLIMITED_USES = 0
MAFIA_EVERY_OTHER_NIGHT = -1

MafiaRole.MAYOR = MafiaRole(
    'VM', 'Mayor', MafiaFaction.VILLAGE,
    [(MafiaActionType.REVEAL, 1)],
    min_in_game=1, max_in_game=1
)
MafiaRole.COP = MafiaRole(
    'VC', 'Cop', MafiaFaction.VILLAGE,
    [(MafiaActionType.INVESTIGATE, MAFIA_UNLIMITED_USES)],
)
MafiaRole.INSANE_COP = MafiaRole(
    'VI', 'Insane Cop', MafiaFaction.VILLAGE,
    [(MafiaActionType.INSANE_INVESTIGATE, MAFIA_UNLIMITED_USES)],
    apparent_name='Cop'
)
MafiaRole.FORGETFUL_COP = MafiaRole(
    'VF',  'Forgetful Cop',  MafiaFaction.VILLAGE,
    [(MafiaActionType.FORGETFUL_INVESTIGATE, MAFIA_UNLIMITED_USES)],
)
MafiaRole.DOCTOR = MafiaRole(
    'VD', 'Doctor', MafiaFaction.VILLAGE,
    [(MafiaActionType.PROTECT, MAFIA_UNLIMITED_USES)],
)
MafiaRole.BUS_DRIVER = MafiaRole(
    'VB', 'Bus Driver', MafiaFaction.VILLAGE,
    [(MafiaActionType.SWITCH, MAFIA_UNLIMITED_USES)],
    max_in_game=1,
)
MafiaRole.TRACKER = MafiaRole(
    'VT',  'Tracker', MafiaFaction.VILLAGE,
    [(MafiaActionType.FOLLOW, MAFIA_UNLIMITED_USES)],
)
MafiaRole.WATCHER = MafiaRole(
    'VW',  'Watcher', MafiaFaction.VILLAGE,
    [(MafiaActionType.WATCH, MAFIA_UNLIMITED_USES)],
)
MafiaRole.ESCORT = MafiaRole(
    'VE',  'Escort', MafiaFaction.VILLAGE,
    [(MafiaActionType.SEDUCE, MAFIA_UNLIMITED_USES)],
    immune_to_seduction=True,
)
MafiaRole.VIGILANTE = MafiaRole(
    'Vi',  'Vigilante', MafiaFaction.VILLAGE,
    [(MafiaActionType.SEDUCE, MAFIA_UNLIMITED_USES)],
)
MafiaRole.VETERAN = MafiaRole(
    'VV',  'Veteran', MafiaFaction.VILLAGE,
    [(MafiaActionType.ON_GUARD, 3)],
)
MafiaRole.MILLER = MafiaRole(
    'Vl',  'Miller', MafiaFaction.VILLAGE,
    [],
    apparent_guilt=MafiaApparentGuilt.GUILTY,
)
MafiaRole.BOMB = MafiaRole(
    'Vo',  'Bomb', MafiaFaction.VILLAGE,
    [],
    immune_to_seduction=True,
    max_in_game=1,
)
MafiaRole.BODYGUARD = MafiaRole(
    'Vg',  'Bodyguard', MafiaFaction.VILLAGE,
    [(MafiaActionType.DEFEND, MAFIA_UNLIMITED_USES)],
)
MafiaRole.DETECTIVE = MafiaRole(
    'Ve',  'Detective', MafiaFaction.VILLAGE,
    [(MafiaActionType.SCRUTINIZE, MAFIA_UNLIMITED_USES)],
)
MafiaRole.BASIC_VILLAGER = MafiaRole(
    'Va', 'Basic Villager', MafiaFaction.VILLAGE,
    []
)
MafiaRole.GODFATHER = MafiaRole(
    'MG', 'Godfather', MafiaFaction.MAFIA,
    [(MafiaActionType.SLAY, MAFIA_UNLIMITED_USES)],
    apparent_guilt=MafiaApparentGuilt.INNOCENT,
    min_in_game=1, max_in_game=1,
)
MafiaRole.LIMO_DRIVER = MafiaRole(
    'ML', 'Limo Driver', MafiaFaction.MAFIA,
    [(MafiaActionType.SWITCH, MAFIA_UNLIMITED_USES)],
    max_in_game=1,
)
MafiaRole.STALKER = MafiaRole(
    'MS', 'Stalker', MafiaFaction.MAFIA,
    [(MafiaActionType.FOLLOW, MAFIA_UNLIMITED_USES)],
)
MafiaRole.LOOKOUT = MafiaRole(
    'Mk', 'Lookout', MafiaFaction.MAFIA,
    [(MafiaActionType.WATCH, MAFIA_UNLIMITED_USES)],
)
MafiaRole.HOOKER = MafiaRole(
    'MH',  'Hooker', MafiaFaction.MAFIA,
    [(MafiaActionType.SEDUCE, MAFIA_UNLIMITED_USES)],
    immune_to_seduction=True,
)
MafiaRole.JANITOR = MafiaRole(
    'MJ', 'Janitor', MafiaFaction.MAFIA,
    [(MafiaActionType.DISPOSE, MAFIA_UNLIMITED_USES)],
)
MafiaRole.FRAMER = MafiaRole(
    'MF', 'Framer', MafiaFaction.MAFIA,
    [(MafiaActionType.FRAME, MAFIA_UNLIMITED_USES)],
)
MafiaRole.YAKUZA = MafiaRole(
    'MY', 'Yakuza', MafiaFaction.MAFIA,
    [(MafiaActionType.CORRUPT, MAFIA_UNLIMITED_USES)],
)
MafiaRole.SABOTEUR = MafiaRole(
    'Ma', 'Saboteur', MafiaFaction.MAFIA,
    [(MafiaActionType.SABOTAGE, MAFIA_UNLIMITED_USES)],
    hidden_to_mafia=True,
)
MafiaRole.SNIPER = MafiaRole(
    'Mi', 'Sniper', MafiaFaction.MAFIA,
    [(MafiaActionType.SNIPE, 1)],
    hidden_to_mafia=True,
)
MafiaRole.BASIC_MAFIA = MafiaRole(
    'Ma', 'Basic Mafia', MafiaFaction.MAFIA,
    [],
    max_in_game=0, # can only be included by corruption
)
MafiaRole.JESTER = MafiaRole(
    'RJ', 'Jester', MafiaFaction.ROGUE,
    [],
)
MafiaRole.SERIAL_KILLER = MafiaRole(
    'RK', 'Serial Killer', MafiaFaction.ROGUE,
    [(MafiaActionType.SLAY, MAFIA_UNLIMITED_USES)],
    night_immune=True,
)
MafiaRole.MASS_MURDERER = MafiaRole(
    'RM', 'Mass Murderer', MafiaFaction.ROGUE,
    [(MafiaActionType.AMBUSH, MAFIA_EVERY_OTHER_NIGHT)],
)
MafiaRole.ARSONIST = MafiaRole(
    'RA', 'Arsonist', MafiaFaction.ROGUE,
    [
        (MafiaActionType.DOUSE, MAFIA_UNLIMITED_USES),
        (MafiaActionType.UN_DOUSE, MAFIA_UNLIMITED_USES),
        (MafiaActionType.IGNITE, MAFIA_UNLIMITED_USES)
    ],
    night_immune=True,
)
MafiaRole.WITCH = MafiaRole(
    'RW', 'Witch', MafiaFaction.ROGUE,
    [(MafiaActionType.CONTROL, MAFIA_UNLIMITED_USES)],
    immune_to_seduction=True,
)
MafiaRole.AMNESIAC = MafiaRole(
    'RE', 'Amnesiac', MafiaFaction.ROGUE,
    [(MafiaActionType.REMEMBER, 1)],
)
MafiaRole.SURVIVOR = MafiaRole(
    'RS', 'Survivor', MafiaFaction.ROGUE,
    [(MafiaActionType.BULLETPROOF_VEST, 3)],
)
MafiaRole.EXECUTIONER = MafiaRole(
    'RX', 'Executioner', MafiaFaction.ROGUE,
    [],
)

class MafiaPlayerStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaPlayerStatus.ALIVE = MafiaPlayerStatus('A', 'Alive')
MafiaPlayerStatus.LYNCHED = MafiaPlayerStatus('L', 'Lynched')
MafiaPlayerStatus.DIED_AT_NIGHT = MafiaPlayerStatus('K', 'Died at Night')

class MafiaPlayer(models.Model):
    game = models.ForeignKey(MafiaGame)
    user = models.ForeignKey(User)
    role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    old_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    older_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    status = models.CharField(
        max_length=MafiaPlayerStatus.CODE_LENGTH,
        choices=MafiaPlayerStatus.get_choice_tuples(),
        default=MafiaPlayerStatus.ALIVE.code
    )
    actions_used_json = models.TextField(default='{}')
    doused = models.BooleanField(default=False)
    executioner_target = models.ForeignKey(User, null=True, related_name='executioner_target')

    def get_actions_used(self):
        return defaultdict(
            (lambda: (0, False)),
            json.loads(self.actions_used_json)
        )

    def mark_action_used(self, action_type_code):
        used = self.get_actions_used()
        used[action_type_code] = (used[action_type_code][0] + 1, True)
        self.actions_used_json = json.dumps(used)

    def mark_night_passed(self):
        used = self.get_actions_used()
        json.dumps({at: (use[0], False) for at, use in used.iteritems()})

    @property
    def revealed_as_mayor(self):
        return self.get_actions_used()[MafiaActionType.REVEAL.code][0] >= 1

class MafiaNightResult(models.Model):
    game = models.ForeignKey(MafiaGame)
    night_number = models.PositiveSmallIntegerField()
    description = models.TextField(default='')

class MafiaAction(models.Model):
    performer = models.ForeignKey(MafiaPlayer)
    night_number = models.PositiveSmallIntegerField()
    action_type = models.CharField(
        max_length=MafiaActionType.CODE_LENGTH,
        choices=MafiaActionType.get_choice_tuples(),
        default=MafiaActionType.NO_ACTION.code
    )
    target0 = models.ForeignKey(User, related_name='target0', null=True)
    target1 = models.ForeignKey(User, related_name='target1', null=True)

class MafiaPlayerNightStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaPlayerNightStatus.SAFE = MafiaPlayerNightStatus('S', 'Safe')
MafiaPlayerNightStatus.ATTACKED = MafiaPlayerNightStatus('A', 'Attacked')
MafiaPlayerNightStatus.TERMINATED = MafiaPlayerNightStatus('T', 'Terimated')

class MafiaPlayerNightResult(models.Model):
    action = models.OneToOneField(MafiaAction)

    controlled_to_target = models.ForeignKey(User, null=True, related_name='controlled_to_target')
    switched_by_json = models.TextField(default='[]')
    switched_with = models.ForeignKey(User, null=True, related_name='switched_with')
    attempted_seduced = models.BooleanField(default=False)
    framed = models.BooleanField(default=False)
    protected_by_json = models.TextField(default='[]')
    defended_by_json = models.TextField(default='[]')
    attempted_corrupted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=MafiaPlayerNightStatus.CODE_LENGTH,
        choices=MafiaPlayerNightStatus.get_choice_tuples(),
        default=MafiaPlayerNightStatus.SAFE.code
    )
    doused = models.BooleanField(default=False)
    un_doused = models.BooleanField(default=False)
    disposed = models.BooleanField(default=False)
    remembered = models.ForeignKey(User, null=True, related_name='remembered')
    action_effective = models.BooleanField(default=False)
    other_targeted_by_json = models.TextField(default='[]')
    report = models.TextField(default='')

    @property
    def player(self):
        return self.action.performer

    @property
    def action_type(self):
        return self.action.action_type

    @property
    def target0(self):
        return self.action.target0

    @property
    def target1(self):
        return self.action.target1

    @property
    def target0_after_control(self):
        return self.controlled_to_target or self.target0

    @property
    def target1_after_control(self):
        return self.target1

    @property
    def apparent_target0(self):
        return None if self.seduced else self.target0_after_control

    @property
    def apparent_target1(self):
        return None if self.seduced else self.target1_after_control

    @property
    def _resisted(self):
        return self.protected or self.defended or self.bulletproof or self.on_guard or (
            MafiaRole.get_instance(self.player.role).night_immune
        )

    @property
    def died(self):
        return (
            self.status == MafiaPlayerNightStatus.TERMINATED or (
                self.status == MafiaPlayerNightStatus.ATTACKED.code and
                not self._resisted
            )
        )

    @property
    def protected(self):
        return len(json.loads(self.protected_by_json)) >= 1

    @property
    def seduced(self):
        return (
            self.attempted_seduced and
            not MafiaRole.get_instance(self.player.role).immune_to_seduction
        )

    @property
    def seduced_or_died(self):
        return self.seduced or self.died

    @property
    def corrupted(self):
        return self.attempted_corrupted and not self._resisted

    @property
    def on_guard(self):
        return self.action_type == MafiaActionType.ON_GUARD.code

    @property
    def bulletproof(self):
        return self.action_type == MafiaActionType.BULLETPROOF_VEST.code

    @property
    def switched_with_or_self(self):
        return self.switched_with or self.player.user

    def add_switched_by(self):
        self.switched_by_json = json.dumps(list(set(
            json.loads(self.switched_by_json) + [user.username]
        )))

    def clear_switched_by(self):
        self.switched_by_json = '[]'
        self.switched_with = None

    def get_switched_by(self):
        return [
            User.get(username=username)
            for username in json.loads(self.switched_by_json)
        ]

    @property
    def times_switched(self):
        return len(json.loads(self.switched_by_json))

    def add_protected_by(self, user):
        self.protected_by_json = json.dumps(list(set(
            json.loads(self.protected_by_json) + [user.username]
        )))

    def get_protected_by(self):
        return [
            User.get(username=username)
            for username in json.loads(self.protected_by_json)
        ]

    def add_defended_by(self, user):
        self.defended_by_json = json.dumps(list(set(
            json.loads(self.defended_by_json) + [user.username]
        )))

    def get_defended_by(self, user):
        return [
            User.get(username=username)
            for username in json.loads(self.defended_by_json)
        ]

    def add_targeted_by(self, user):
        self.other_targeted_by_json = json.dumps(list(set(
            json.loads(self.other_targeted_by_json) + [user.username]
        )))

    def get_targeted_by(self):
        return [
            User.get(username=username)
            for username in (
                json.loads(self.switched_by_json) +
                json.loads(self.protected_by_json) +
                json.loads(self.defended_by_json) +
                json.loads(self.other_targeted_by_json)
            )
        ]

    def add_report_line(self, line):
        if self.report:
            self.report += '\n'
        self.report += line

    def contains_report_line(self, line):
        return line in self.report.splitlines()

class MafiaVoteType(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaVoteType.ABSTAIN = MafiaVoteType('A', 'Abstain')
MafiaVoteType.NO_LYNCH = MafiaVoteType('N', 'No Lynch')
MafiaVoteType.LYNCH = MafiaVoteType('L', 'Lynch')

class MafiaVote(models.Model):
    voter = models.ForeignKey(MafiaPlayer)
    day_number = models.PositiveSmallIntegerField()
    vote_type = models.CharField(
        max_length=MafiaVoteType.CODE_LENGTH,
        choices=MafiaVoteType.get_choice_tuples(),
        default=MafiaVoteType.ABSTAIN.code
    )
    vote = models.ForeignKey(User, null=True)
    comment = models.TextField(default='')

class MafiaDayResult(models.Model):
    game = models.ForeignKey(MafiaGame)
    day_number = models.PositiveSmallIntegerField()
    lynched = models.ForeignKey(User, null=True)
    description = models.TextField(default="")

class MafiaError(Exception):
    pass
