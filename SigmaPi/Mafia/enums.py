# -*- coding: UTF-8 -*-

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

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__class__.__name__ + '(\'' + self.code + \
            '\', \'' + self.name + '\')'

    def __unicode__(self):
        return unicode(str(self))

class MafiaGameStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

class MafiaGameTime(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaGameTime.DAWN = MafiaGameTime('A', 'Dawn')
MafiaGameTime.DAY = MafiaGameTime('D', 'Day')
MafiaGameTime.DUSK = MafiaGameTime('U', 'Dusk')
MafiaGameTime.NIGHT = MafiaGameTime('N', 'Night')

class MafiaFaction(object):
    VILLAGE = 'Village'
    MAFIA = 'Mafia'
    ROGUE = 'Rogue'

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

class MafiaVoteType(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaVoteType.ABSTAIN = MafiaVoteType('A', 'Abstain')
MafiaVoteType.NO_LYNCH = MafiaVoteType('N', 'No Lynch')
MafiaVoteType.LYNCH = MafiaVoteType('L', 'Lynch')
