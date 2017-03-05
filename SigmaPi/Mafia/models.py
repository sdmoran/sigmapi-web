
from django.db import models
from django.contrib.auth.models import User

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

class MafiaActionType(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, num_targets, apparant_name=None, targets_dead=False):
        super(MafiaActionType, self).__init__(code, name)
        self.num_targets = num_targets
        self.apparant_name = apparant_name or name
        self.targets_dead = targets_dead

MafiaActionType.REVEAL = MafiaActionType('Re', 'Reveal', 0)
MafiaActionType.INVESTIGATE = MafiaActionType('In', 'Investigate', 1)
MafiaActionType.INSANE_INVESTIGATE = MafiaActionType('II', 'Insane Investigate', 1, apparant_name='Investigate')
MafiaActionType.FORGETFUL_INVESTIGATE = MafiaActionType('FI', 'Forgetful Investigate', 1)
MafiaActionType.PROTECT = MafiaActionType('Pr', 'Protect', 1)
MafiaActionType.SWITCH = MafiaActionType('Sw', 'Switch', 2)
MafiaActionType.FOLLOW = MafiaActionType('Fo', 'Follow', 1)
MafiaActionType.WATCH = MafiaActionType('Wa', 'Watch', 1)
MafiaActionType.SEDUCE = MafiaActionType('Se', 'Seduce', 1)
MafiaActionType.SLAY = MafiaActionType('Sl', 'Slay', 1)
MafiaActionType.ON_GUARD = MafiaActionType('OG', 'On Guard', 0)
MafiaActionType.DEFEND = MafiaActionType('De', 'Defend', 1)
MafiaActionType.SCRUTINIZE = MafiaActionType('Sc', 'Scrutinize', 1)
MafiaActionType.DISPOSE = MafiaActionType('Di', 'Dispose', 1)
MafiaActionType.FRAME = MafiaActionType('Fr', 'Frame', 1)
MafiaActionType.CORRUPT = MafiaActionType('Co', 'Corrupt', 1)
MafiaActionType.SABOTAGE = MafiaActionType('Sa', 'Sabotage', 1)
MafiaActionType.SNIPE = MafiaActionType('Sn', 'Snipe', 1)
MafiaActionType.AMBUSH = MafiaActionType('Am', 'Ambush', 1)
MafiaActionType.DOUSE = MafiaActionType('Do', 'Douse', 1)
MafiaActionType.UN_DOUSE = MafiaActionType('UD', 'Un-Douse', 1)
MafiaActionType.IGNITE = MafiaActionType('Ig', 'Ignite', 0)
MafiaActionType.CONTROL = MafiaActionType('Co', 'Control', 2)
MafiaActionType.REMEMBER = MafiaActionType('Re', 'Remember', 1, targets_dead=True)
MafiaActionType.BULLETPROOF_VEST = MafiaActionType('BV', 'Bulletproof Vest', 0)

class MafiaRole(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, faction, actions, apparant_name=None):
        super(MafiaRole, self).__init__(code, name)
        self.faction = faction
        self.actions = actions
        self.apparant_name = apparant_name or name

MafiaRole.MAYOR = MafiaRole(
    'VM', 'Mayor', MafiaFaction.VILLAGE,
    [MafiaActionType.REVEAL],
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
)
MafiaRole.TRACKER = MafiaRole(
    'VT',  'Tracker', MafiaFaction.VILLAGE,
    [MafiaActionType.FOLLOW]
)
MafiaRole.WATCHER = MafiaRole(
    'VW',  'Watcher', MafiaFaction.VILLAGE,
    [MafiaActionType.WATCH]
)
MafiaRole.ESCORT = MafiaRole(
    'VE',  'Escort', MafiaFaction.VILLAGE,
    [MafiaActionType.SEDUCE]
)
MafiaRole.VIGILANTE = MafiaRole(
    'VG',  'Vigilante', MafiaFaction.VILLAGE,
    [MafiaActionType.SEDUCE]
)
MafiaRole.VETERAN = MafiaRole(
    'VV',  'Veteran', MafiaFaction.VILLAGE,
    [MafiaActionType.ON_GUARD]
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
    [MafiaActionType.DEFEND]
)
MafiaRole.DETECTIVE = MafiaRole(
    'VE',  'Detective', MafiaFaction.VILLAGE,
    [MafiaActionType.SCRUTINIZE]
)
MafiaRole.GODFATHER = MafiaRole(
    'MG', 'Godfather', MafiaFaction.MAFIA,
    [MafiaActionType.SLAY],
)
MafiaRole.LIMO_DRIVER = MafiaRole(
    'ML', 'Limo Driver', MafiaFaction.MAFIA,
    [MafiaActionType.SWITCH],
)
MafiaRole.STALKER = MafiaRole(
    'MS', 'Stalker', MafiaFaction.MAFIA,
    [MafiaActionType.FOLLOW],
)
MafiaRole.LOOKOUT = MafiaRole(
    'MK', 'Lookout', MafiaFaction.MAFIA,
    [MafiaActionType.WATCH],
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
)
MafiaRole.JESTER = MafiaRole(
    'RJ', 'Jester', MafiaFaction.ROGUE,
    [],
)
MafiaRole.SERIAL_KILLER = MafiaRole(
    'RK', 'Serial Killer', MafiaFaction.ROGUE,
    [MafiaActionType.SLAY],
)
MafiaRole.MASS_MURDERER = MafiaRole(
    'RM', 'Mass Murderer', MafiaFaction.ROGUE,
    [MafiaActionType.AMBUSH],
)
MafiaRole.ARSONIST = MafiaRole(
    'RA', 'Arsonist', MafiaFaction.ROGUE,
    [MafiaActionType.DOUSE, MafiaActionType.UN_DOUSE, MafiaActionType.IGNITE],
)
MafiaRole.WITCH = MafiaRole(
    'RW', 'Witch', MafiaFaction.ROGUE,
    [MafiaActionType.CONTROL],
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
MafiaPlayerStatus.KILLED = MafiaPlayerStatus('K', 'Killed')

class MafiaPlayer(models.Model):
    game = models.ForeignKey(MafiaGame)
    player = models.ForeignKey(User)
    previous_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        default=None
    )
    role = models.CharField(max_length=2, choices=MafiaRole.get_choice_tuples())
    times_action_used = models.IntegerField(default=0)
    doused = models.BooleanField(default=False)
    status = models.CharField(
        max_length=MafiaPlayerStatus.CODE_LENGTH,
        choices=MafiaPlayerStatus.get_choice_tuples(),
        default=MafiaPlayerStatus.ALIVE.code
    )
    executioner_target = models.ForeignKey(User, null=True, related_name='executioner_target')

class MafiaAction(models.Model):
    game = models.ForeignKey(MafiaGame)
    player = models.ForeignKey(User)
    action_type = models.CharField(
        max_length=MafiaActionType.CODE_LENGTH,
        choices=MafiaActionType.get_choice_tuples()
    )
    target1 = models.ForeignKey(User, related_name='target1', default=None)
    target2 = models.ForeignKey(User, related_name='target2', default=None)
    target3 = models.ForeignKey(User, related_name='target3', default=None)
