
from django.db import models
from django.contrib.auth.models import User
import json

class ChoiceEnumeration(object):

    def __init__(self, name, code):
        self.name = name
        self.code = code

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

class MafiaGameTime(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaGameTime.DAWN = MafiaGameTime('A', 'Dawn')
MafiaGameTime.DUSK = MafiaGameTime('U', 'Dusk')

class MafiaGame(models.Model):
    created = models.DateField()
    day_number = models.PositiveSmallIntegerField(default=1)
    time = models.CharField(
        max_length=MafiaGameTime.CODE_LENGTH,
        choices=MafiaGameTime.get_choice_tuples(),
        default=MafiaGameTime.DUSK
    )

class MafiaFaction(object):
    VILLAGE = 'V'
    MAFIA = 'M'
    ROGUE = 'R'

class MafiaActionType(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, targets_can_be_self,
                 apparant_name=None, targets_dead=False,
                 can_target_self=True, is_direct_offense=False,
                 is_lethal=False, is_covert=False):
        super(MafiaActionType, self).__init__(code, name)
        self.targets_can_be_self = targets_can_be_self
        self.apparant_name = apparant_name or name
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
MafiaActionType.INSANE_INVESTIGATE = MafiaActionType('II', 'Insane Investigate', [False], apparant_name='Investigate')
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

class MafiaRole(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, faction, action_types, apparant_name=None,
                 night_immune=False, immune_to_seduction=False,
                 min_in_game=0, max_in_game=float('inf')):
        super(MafiaRole, self).__init__(code, name)
        self.faction = faction
        self.action_types = action_types
        self.apparant_name = apparant_name or name

MafiaRole.MAYOR = MafiaRole(
    'VM', 'Mayor', MafiaFaction.VILLAGE,
    [MafiaActionType.REVEAL],
    min_in_game=1, max_in_game=1
)
MafiaRole.COP = MafiaRole(
    'VC', 'Cop', MafiaFaction.VILLAGE,
    [MafiaActionType.INVESTIGATE],
)
MafiaRole.INSANE_COP = MafiaRole(
    'VI', 'Insane Cop', MafiaFaction.VILLAGE,
    [MafiaActionType.INSANE_INVESTIGATE],
    apparant_name='Cop'
)
MafiaRole.FORGETFUL_COP = MafiaRole(
    'VF',  'Forgetful Cop',  MafiaFaction.VILLAGE,
    [MafiaActionType.FORGETFUL_INVESTIGATE],
)
MafiaRole.DOCTOR = MafiaRole(
    'VD', 'Doctor', MafiaFaction.VILLAGE,
    [MafiaActionType.PROTECT],
)
MafiaRole.BUS_DRIVER = MafiaRole(
    'VB', 'Bus Driver', MafiaFaction.VILLAGE,
    [MafiaActionType.SWITCH],
    max_in_game=1,
)
MafiaRole.TRACKER = MafiaRole(
    'VT',  'Tracker', MafiaFaction.VILLAGE,
    [MafiaActionType.FOLLOW],
)
MafiaRole.WATCHER = MafiaRole(
    'VW',  'Watcher', MafiaFaction.VILLAGE,
    [MafiaActionType.WATCH],
)
MafiaRole.ESCORT = MafiaRole(
    'VE',  'Escort', MafiaFaction.VILLAGE,
    [MafiaActionType.SEDUCE],
    immune_to_seduction=True,
)
MafiaRole.VIGILANTE = MafiaRole(
    'VG',  'Vigilante', MafiaFaction.VILLAGE,
    [MafiaActionType.SEDUCE],
)
MafiaRole.VETERAN = MafiaRole(
    'VV',  'Veteran', MafiaFaction.VILLAGE,
    [MafiaActionType.ON_GUARD],
)
MafiaRole.MILLER = MafiaRole(
    'VL',  'Miller', MafiaFaction.VILLAGE,
    [],
)
MafiaRole.BOMB = MafiaRole(
    'VB',  'Bomb', MafiaFaction.VILLAGE,
    [],
    immune_to_seduction=True,
    max_in_game=1,
)
MafiaRole.BODYGUARD = MafiaRole(
    'VO',  'Bodyguard', MafiaFaction.VILLAGE,
    [MafiaActionType.DEFEND],
)
MafiaRole.DETECTIVE = MafiaRole(
    'VE',  'Detective', MafiaFaction.VILLAGE,
    [MafiaActionType.SCRUTINIZE],
)
MafiaRole.GODFATHER = MafiaRole(
    'MG', 'Godfather', MafiaFaction.MAFIA,
    [MafiaActionType.SLAY],
    min_in_game=1, max_in_game=1,
)
MafiaRole.LIMO_DRIVER = MafiaRole(
    'ML', 'Limo Driver', MafiaFaction.MAFIA,
    [MafiaActionType.SWITCH],
    max_in_game=1,
)
MafiaRole.STALKER = MafiaRole(
    'MS', 'Stalker', MafiaFaction.MAFIA,
    [MafiaActionType.FOLLOW],
)
MafiaRole.LOOKOUT = MafiaRole(
    'MK', 'Lookout', MafiaFaction.MAFIA,
    [MafiaActionType.WATCH],
)
MafiaRole.HOOKER = MafiaRole(
    'MH',  'Hooker', MafiaFaction.MAFIA,
    [MafiaActionType.SEDUCE],
    immune_to_seduction=True,
)
MafiaRole.JANITOR = MafiaRole(
    'MJ', 'Janitor', MafiaFaction.MAFIA,
    [MafiaActionType.DISPOSE],
)
MafiaRole.FRAMER = MafiaRole(
    'MF', 'Framer', MafiaFaction.MAFIA,
    [MafiaActionType.FRAME],
)
MafiaRole.YAKUZA = MafiaRole(
    'MY', 'Yakuza', MafiaFaction.MAFIA,
    [MafiaActionType.CORRUPT],
)
MafiaRole.SABOTEUR = MafiaRole(
    'MA', 'Saboteur', MafiaFaction.MAFIA,
    [MafiaActionType.SABOTAGE],
)
MafiaRole.SNIPER = MafiaRole(
    'MI', 'Sniper', MafiaFaction.MAFIA,
    [MafiaActionType.SNIPE],
)
MafiaRole.BASIC_MAFIA = MafiaRole(
    'MB', 'Basic Mafia', MafiaFaction.MAFIA,
    [],
    max_in_game=0, # can only be included by corruption
)
MafiaRole.JESTER = MafiaRole(
    'RJ', 'Jester', MafiaFaction.ROGUE,
    [],
)
MafiaRole.SERIAL_KILLER = MafiaRole(
    'RK', 'Serial Killer', MafiaFaction.ROGUE,
    [MafiaActionType.SLAY],
    night_immune=True,
)
MafiaRole.MASS_MURDERER = MafiaRole(
    'RM', 'Mass Murderer', MafiaFaction.ROGUE,
    [MafiaActionType.AMBUSH],
)
MafiaRole.ARSONIST = MafiaRole(
    'RA', 'Arsonist', MafiaFaction.ROGUE,
    [MafiaActionType.DOUSE, MafiaActionType.UN_DOUSE, MafiaActionType.IGNITE],
    night_immune=True,
)
MafiaRole.WITCH = MafiaRole(
    'RW', 'Witch', MafiaFaction.ROGUE,
    [MafiaActionType.CONTROL],
    immune_to_seduction=True,
)
MafiaRole.AMNESIAC = MafiaRole(
    'RE', 'Amnesiac', MafiaFaction.ROGUE,
    [MafiaActionType.REMEMBER],
)
MafiaRole.SURVIVOR = MafiaRole(
    'RS', 'Survivor', MafiaFaction.ROGUE,
    [MafiaActionType.BULLETPROOF_VEST],
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
    previous_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        default=None
    )
    role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples()
    )
    times_action_used = models.SmallIntegerField(default=0)
    doused = models.BooleanField(default=False)
    status = models.CharField(
        max_length=MafiaPlayerStatus.CODE_LENGTH,
        choices=MafiaPlayerStatus.get_choice_tuples(),
        default=MafiaPlayerStatus.ALIVE.code
    )
    executioner_target = models.ForeignKey(User, null=True, related_name='executioner_target')

class MafiaNightStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaNightStatus.SAFE = MafiaNightStatus('N', 'Not Attacked')
MafiaNightStatus.ATTACKED = MafiaNightStatus('A', 'Attacked')
MafiaNightStatus.TERMINATED = MafiaNightStatus('T', 'Terimated')

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

class MafiaNightResult(models.Model):
    action = models.OneToOneField(MafiaAction)

    switched_by_json = models.TextField(default='[]')
    protected_by_json = models.TextField(default='[]')
    defended_by_json = models.TextField(default='[]')
    other_targeted_by_json = models.TextField(default='[]')
    controlled_to_target = models.ForeignKey(User, null=True, related_name='controlled_to_target')
    switched_with = models.ForeignKey(User, null=True, related_name='switched_with')
    remembered = models.ForeignKey(User, null=True, related_name='remembered')
    status = models.CharField(
        max_length=MafiaNightStatus.CODE_LENGTH,
        choices=MafiaNightStatus.get_choice_tuples(),
        default=MafiaNightStatus.SAFE.code
    )
    attempted_seduced = models.BooleanField(default=False)
    framed = models.BooleanField(default=False)
    attempted_corrupted = models.BooleanField(default=False)
    doused = models.BooleanField(default=False)
    un_doused = models.BooleanField(default=False)
    disposed = models.BooleanField(default=False)
    action_effective = models.BooleanField(default=False)
    report = models.TextField(default="")

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
    def target0(self):
        return self.action.target1

    @property
    def target0_after_control(self):
        return self.controlled_to_target or self.target0

    @property
    def target1_after_control(self):
        return self.target1

    @property
    def apparant_target0(self):
        return None if self.seduced else self.target0_after_control

    @property
    def apparant_target1(self):
        return None if self.seduced else self.target1_after_control

    @property
    def _resisted(self):
        return self.protected or self.defended or self.bulletproof or self.on_guard or (
            MafiaRole.get_instance(self.player.role).night_immune
        )

    @property
    def died(self):
        return (
            self.status == MafiaNightStatus.TERMINATED or (
                self.status == MafiaNightStatus.ATTACKED.code and
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

    def add_switched_by(self, user):
        self.switched_by_json = json.dumps(list(set(
            json.loads(self.switched_by_json) + [user.username]
        )))

    def clear_switched_by(self):
        self.switched_by_json = '[]'
        self.switched_with = None

    def add_targeted_by(self, user):
        self.other_targeted_by_json = json.dumps(list(set(
            json.loads(self.other_targeted_by_json) + [user.username]
        )))

    def add_protected_by(self, user):
        self.protected_by_json = json.dumps(list(set(
            json.loads(self.protected_by_json) + [user.username]
        )))

    def get_protected_by(self, user):
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
            self.report += "\n"
        self.report += line

class MafiaError(Exception):
    pass
