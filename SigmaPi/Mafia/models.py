
from django.db import models
from django.contrib.auth.models import User

class MafiaGame(models.Model):
    created = models.DateField()

class MafiaFaction(object):
    VILLAGE = 'V'
    MAFIA = 'M'
    ROGUE = 'R'

class ChoiceEnumeration(object):

    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    @classmethod
    def get_instances(cls):
        return [
            getattr(cls, attr) for attr in dir(cls)
            if getattr(cls, attr).__class__ is cls
        ]

    @classmethod
    def get_instance(cls, abbreviation):
        for inst in cls.get_instances():
            if inst.abbreviation == abbreviation:
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
            (inst.abbreviation, inst.name)
            for inst in cls.get_instances()
        ]

class MafiaAction(ChoiceEnumeration):

    def __init__(self, abbreviation, name, num_targets, apparant_name=None, targets_dead=False):
        super(MafiaAction, self).__init__(abbreviation, name)
        self.num_targets = num_targets
        self.apparant_name = apparant_name or name
        self.targets_dead = targets_dead

MafiaAction.REVEAL = MafiaAction('Re', 'Reveal', 0)
MafiaAction.INVESTIGATE = MafiaAction('In', 'Investigate', 1)
MafiaAction.INSANE_INVESTIGATE = MafiaAction('II', 'Insane Investigate', 1, apparant_name='Investigate')
MafiaAction.FORGETFUL_INVESTIGATE = MafiaAction('FI', 'Forgetful Investigate', 1)
MafiaAction.PROTECT = MafiaAction('Pr', 'Protect', 1)
MafiaAction.SWITCH = MafiaAction('Sw', 'Switch', 2)
MafiaAction.FOLLOW = MafiaAction('Fo', 'Follow', 1)
MafiaAction.WATCH = MafiaAction('Wa', 'Watch', 1)
MafiaAction.SEDUCE = MafiaAction('Se', 'Seduce', 1)
MafiaAction.SLAY = MafiaAction('Sl', 'Slay', 1)
MafiaAction.ON_GUARD = MafiaAction('OG', 'On Guard', 0)
MafiaAction.DEFEND = MafiaAction('De', 'Defend', 1)
MafiaAction.SCRUTINIZE = MafiaAction('Sc', 'Scrutinize', 1)
MafiaAction.DISPOSE = MafiaAction('Di', 'Dispose', 1)
MafiaAction.FRAME = MafiaAction('Fr', 'Frame', 1)
MafiaAction.CORRUPT = MafiaAction('Co', 'Corrupt', 1)
MafiaAction.SABOTAGE = MafiaAction('Sa', 'Sabotage', 1)
MafiaAction.SNIPE = MafiaAction('Sn', 'Snipe', 1)
MafiaAction.AMBUSH = MafiaAction('Am', 'Ambush', 1)
MafiaAction.DOUSE = MafiaAction('Do', 'Douse', 1)
MafiaAction.UN_DOUSE = MafiaAction('UD', 'Un-Douse', 1)
MafiaAction.IGNITE = MafiaAction('Ig', 'Ignite', 0)
MafiaAction.CONTROL = MafiaAction('Co', 'Control', 2)
MafiaAction.REMEMBER = MafiaAction('Re', 'Remember', 1, targets_dead=True)
MafiaAction.BULLETPROOF_VEST = MafiaAction('BV', 'Bulletproof Vest', 0)

class MafiaRole(ChoiceEnumeration):

    def __init__(self, abbreviation, name, faction, actions, apparant_name=None):
        super(MafiaRole, self).__init__(abbreviation, name)
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
)
MafiaRole.MASS_MURDERER = MafiaRole(
    'RM', 'Mass Murderer', MafiaFaction.ROGUE,
    [MafiaAction.AMBUSH],
)
MafiaRole.ARSONIST = MafiaRole(
    'RA', 'Arsonist', MafiaFaction.ROGUE,
    [MafiaAction.DOUSE, MafiaAction.UN_DOUSE, MafiaAction.IGNITE],
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

class MafiaPlayerState(models.Model):
    game = models.ForeignKey(MafiaGame)
    player = models.ForeignKey(User)
    previous_role = models.CharField(max_length=2, choices=MafiaRole.get_choice_tuples(), default=None)
    role = models.CharField(max_length=2, choices=MafiaRole.get_choice_tuples())
    times_action_used = models.IntegerField(default=0)
    doused = models.BooleanField(default=False)
    executioner_target = models.ForeignKey(User, null=True, related_name='executioner_target')
