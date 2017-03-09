
from django.db import models
from django.contrib.auth.models import User
import json

class MafiaGame(models.Model):
    created = models.DateField()

class MafiaFaction(object):
    VILLAGE = 'V'
    MAFIA = 'M'
    ROGUE = 'R'

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

class MafiaAction(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, num_targets, 
                 apparant_name=None, targets_dead=False, 
                 can_target_self=True, appears_targeting_self=False):
        super(MafiaAction, self).__init__(code, name)
        self.num_targets = num_targets
        self.apparant_name = apparant_name or name
        self.targets_dead = targets_dead
        self.can_target_self = can_target_self
        self.appears_targeting_self = appears_targeting_self
        if self.appears_targeting_self and self.num_targets > 0:
            raise ValueError("appears_targeting_self can only be True when num_targets == 0")

MafiaAction.NO_ACTION = MafiaAction('NA', 'No Action', 0)
MafiaAction.SEDUCE = MafiaAction('Se', 'Seduce', 1)
MafiaAction.REMEMBER = MafiaAction('Re', 'Remember', 1, targets_dead=True)
MafiaAction.ON_GUARD = MafiaAction('OG', 'On Guard', 0, appears_targeting_self=True)
MafiaAction.SWITCH = MafiaAction('Sw', 'Switch', 2)
MafiaAction.CONTROL = MafiaAction('Co', 'Control', 2, can_target_self=False)
MafiaAction.FRAME = MafiaAction('Fr', 'Frame', 1)
MafiaAction.INVESTIGATE = MafiaAction('In', 'Investigate', 1, can_target_self=False)
MafiaAction.INSANE_INVESTIGATE = MafiaAction('II', 'Insane Investigate', 1, apparant_name='Investigate', can_target_self=False)
MafiaAction.FORGETFUL_INVESTIGATE = MafiaAction('FI', 'Forgetful Investigate', 1)
MafiaAction.SCRUTINIZE = MafiaAction('Sc', 'Scrutinize', 1)
MafiaAction.PROTECT = MafiaAction('Pr', 'Protect', 1, can_target_self=False)
MafiaAction.DEFEND = MafiaAction('De', 'Defend', 1)
MafiaAction.BULLETPROOF_VEST = MafiaAction('BV', 'Bulletproof Vest', 0, appears_targeting_self=True)
MafiaAction.CORRUPT = MafiaAction('Co', 'Corrupt', 1, can_target_self=False)
MafiaAction.SLAY = MafiaAction('Sl', 'Slay', 1)
MafiaAction.IGNITE = MafiaAction('Ig', 'Ignite', 0)
MafiaAction.SNIPE = MafiaAction('Sn', 'Snipe', 1)
MafiaAction.SABOTAGE = MafiaAction('Sa', 'Sabotage', 1)
MafiaAction.AMBUSH = MafiaAction('Am', 'Ambush', 1)
MafiaAction.DOUSE = MafiaAction('Do', 'Douse', 1)
MafiaAction.UN_DOUSE = MafiaAction('UD', 'Un-Douse', 1)
MafiaAction.DISPOSE = MafiaAction('Di', 'Dispose', 1)
MafiaAction.REVEAL = MafiaAction('Re', 'Reveal', 0)
MafiaAction.FOLLOW = MafiaAction('Fo', 'Follow', 1)
MafiaAction.WATCH = MafiaAction('Wa', 'Watch', 1)

class MafiaRole(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, faction, actions, apparant_name=None, night_immune=False):
        super(MafiaRole, self).__init__(code, name)
        self.faction = faction
        self.actions = actions
        self.apparant_name = apparant_name or name

MafiaRole.MAYOR = MafiaRole(
    'VM', 'Mayor', MafiaFaction.VILLAGE,
    [MafiaAction.REVEAL],
)
MafiaRole.COP = MafiaRole(
    'VC', 'Cop', MafiaFaction.VILLAGE,
    [MafiaAction.INVESTIGATE],
)
MafiaRole.INSANE_COP = MafiaRole(
    'VI', 'Insane Cop', MafiaFaction.VILLAGE,
    [MafiaAction.INSANE_INVESTIGATE],
    apparant_name='Cop'
)
MafiaRole.FORGETFUL_COP = MafiaRole(
    'VF',  'Forgetful Cop',  MafiaFaction.VILLAGE,
    [MafiaAction.FORGETFUL_INVESTIGATE],
)
MafiaRole.DOCTOR = MafiaRole(
    'VD', 'Doctor', MafiaFaction.VILLAGE,
    [MafiaAction.PROTECT],
)
MafiaRole.BUS_DRIVER = MafiaRole(
    'VB', 'Bus Driver', MafiaFaction.VILLAGE,
    [MafiaAction.SWITCH],
)
MafiaRole.TRACKER = MafiaRole(
    'VT',  'Tracker', MafiaFaction.VILLAGE,
    [MafiaAction.FOLLOW]
)
MafiaRole.WATCHER = MafiaRole(
    'VW',  'Watcher', MafiaFaction.VILLAGE,
    [MafiaAction.WATCH]
)
MafiaRole.ESCORT = MafiaRole(
    'VE',  'Escort', MafiaFaction.VILLAGE,
    [MafiaAction.SEDUCE]
)
MafiaRole.VIGILANTE = MafiaRole(
    'VG',  'Vigilante', MafiaFaction.VILLAGE,
    [MafiaAction.SEDUCE]
)
MafiaRole.VETERAN = MafiaRole(
    'VV',  'Veteran', MafiaFaction.VILLAGE,
    [MafiaAction.ON_GUARD]
)
MafiaRole.MILLER = MafiaRole(
    'VL',  'Miller', MafiaFaction.VILLAGE,
    []
)
MafiaRole.BOMB = MafiaRole(
    'VB',  'Bomb', MafiaFaction.VILLAGE,
    []
)
MafiaRole.BODYGUARD = MafiaRole(
    'VO',  'Bodyguard', MafiaFaction.VILLAGE,
    [MafiaAction.DEFEND]
)
MafiaRole.DETECTIVE = MafiaRole(
    'VE',  'Detective', MafiaFaction.VILLAGE,
    [MafiaAction.SCRUTINIZE]
)
MafiaRole.GODFATHER = MafiaRole(
    'MG', 'Godfather', MafiaFaction.MAFIA,
    [MafiaAction.SLAY],
)
MafiaRole.LIMO_DRIVER = MafiaRole(
    'ML', 'Limo Driver', MafiaFaction.MAFIA,
    [MafiaAction.SWITCH],
)
MafiaRole.STALKER = MafiaRole(
    'MS', 'Stalker', MafiaFaction.MAFIA,
    [MafiaAction.FOLLOW],
)
MafiaRole.LOOKOUT = MafiaRole(
    'MK', 'Lookout', MafiaFaction.MAFIA,
    [MafiaAction.WATCH],
)
MafiaRole.JANITOR = MafiaRole(
    'MJ', 'Janitor', MafiaFaction.MAFIA,
    [MafiaAction.DISPOSE],
)
MafiaRole.FRAMER = MafiaRole(
    'MF', 'Framer', MafiaFaction.MAFIA,
    [MafiaAction.FRAME],
)
MafiaRole.YAKUZA = MafiaRole(
    'MY', 'Yakuza', MafiaFaction.MAFIA,
    [MafiaAction.CORRUPT],
)
MafiaRole.SABOTEUR = MafiaRole(
    'MA', 'Saboteur', MafiaFaction.MAFIA,
    [MafiaAction.SABOTAGE],
)
MafiaRole.SNIPER = MafiaRole(
    'MI', 'Sniper', MafiaFaction.MAFIA,
    [MafiaAction.SNIPE],
)
MafiaRole.BASIC_MAFIA = MafiaRole(
    'MB', 'Basic Mafia', MafiaFaction.MAFIA,
    [],
)
MafiaRole.JESTER = MafiaRole(
    'RJ', 'Jester', MafiaFaction.ROGUE,
    [],
)
MafiaRole.SERIAL_KILLER = MafiaRole(
    'RK', 'Serial Killer', MafiaFaction.ROGUE,
    [MafiaAction.SLAY],
    night_immune=True,
)
MafiaRole.MASS_MURDERER = MafiaRole(
    'RM', 'Mass Murderer', MafiaFaction.ROGUE,
    [MafiaAction.AMBUSH],
)
MafiaRole.ARSONIST = MafiaRole(
    'RA', 'Arsonist', MafiaFaction.ROGUE,
    [MafiaAction.DOUSE, MafiaAction.UN_DOUSE, MafiaAction.IGNITE],
    night_immune=True
)
MafiaRole.WITCH = MafiaRole(
    'RW', 'Witch', MafiaFaction.ROGUE,
    [MafiaAction.CONTROL],
)
MafiaRole.AMNESIAC = MafiaRole(
    'RE', 'Amnesiac', MafiaFaction.ROGUE,
    [MafiaAction.REMEMBER],
)
MafiaRole.SURVIVOR = MafiaRole(
    'RS', 'Survivor', MafiaFaction.ROGUE,
    [MafiaAction.BULLETPROOF_VEST],
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

class MafiaAttackedStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaAttackedStatus.NOT_ATTACKED = MafiaAttackedStatus('N', 'Not Attacked')
MafiaAttackedStatus.ATTACKED = MafiaAttackedStatus('A', 'Attacked')
MafiaAttackedStatus.ATTACKED_PAST_PROTECTION = MafiaAttackedStatus('P', 'Attacked Past Protection')

class MafiaPlayerNight(models.Model):
    player = models.ForeignKey(MafiaPlayer)
    night = models.PositiveSmallIntegerField()
    action = models.CharField(
        max_length=MafiaAction.CODE_LENGTH,
        choices=MafiaAction.get_choice_tuples(),
        default=MafiaAction.NO_ACTION.code
    )
    target0 = models.ForeignKey(User, related_name='target0', null=True)
    target1 = models.ForeignKey(User, related_name='target1', null=True)

    controlled_by_json = models.TextField(default='[]')
    switched_by_json = models.TextField(default='[]')
    seduced_by_json = models.TextField(default='[]')
    other_targeted_by_json = models.TextField(default='[]')

    controlled_to_target = models.ForeignKey(User, null=True, related_name='controlled_to_target')
    switched_with = models.ForeignKey(User, null=True, related_name='switched_with')
    attacked_status = models.CharField(
        max_length=MafiaAttackedStatus.CODE_LENGTH,
        choices=MafiaAttackedStatus.get_choice_tuples(),
        default=MafiaAttackedStatus.NOT_ATTACKED.code
    )
    protected = models.BooleanField(default=False)

    defended = models.BooleanField(default=False)
    on_guard = models.BooleanField(default=False)
    framed = models.BooleanField(default=False)
    attempted_corrupted = models.BooleanField(default=False)
    doused = models.BooleanField(default=False)
    un_doused = models.BooleanField(default=False)
    disposed = models.BooleanField(default=False)
    died_for_other_reason = models.BooleanField(default=False)

    successfully_performed_dispose = models.BooleanField(default=False)

    @property
    def target0_after_control(self):
        return self.controlled_to_target or self.target0

    @property
    def apparant_target0(self):
        if self.seduced:
            return None
        elif action.appears_targeting_self:
            return player
        elif controlled_to_target:
            return controlled_to_target
        else:
            return target0

    @property
    def _resisted(self):
        return self.protected or self.defended or self.player.night_immune

    @property
    def died(self):
        return (
            (self.attacked_status == MafiaAttackedStatus.ATTACKED.code and not self._resisted) or
            self.attacked_status == MafiaAttackedStatus.ATTACKED_PAST_PROTECTION or
            self.died_for_other_reason
        )

    @property
    def corrupted(self):
        return self.attempted_corrupted and not self._resisted

    def add_controlled_by(self, user):
        self.controlled_by_json = json.dumps(list(set(
            json.loads(self.controlled_by_json) + [user.username]
        )))
        
    def clear_control(self):
        self.controlled_by_json = '[]'
        self.controlled_to_target = None

    def add_switched_by(self, user):
        self.switched_by_json = json.dumps(list(set(
            json.loads(self.switched_by_json) + [user.username]
        )))

    def clear_switch(self):
        self.switched_by_json = '[]'
        self.switched_with = None

    def add_seduced_by(self, user):
        self.switched_by_json = json.dumps(list(set(
            json.loads(self.switched_by_json) + [user.username]
        )))

    @property
    def seduced(self):
        return len(json.loads(self.seduced_by_json)) > 0

    def add_other_targeted_by(self, user):
        self.targeted_by_json = json.dumps(list(set(
            json.loads(self.targeted_by_json) + [user.username]
        )))

    def get_targeted_by(self):
        return [
            User.get(username=username)
            for username in (
                json.loads(self.seduced_by_json) + 
                json.loads(self.switched_by_json) +
                json.loads(self.controlled_by_json) +
                json.loads(self.other_targeted_by_json)
            )
        ] 

class MafiaError(Exception):
    pass
