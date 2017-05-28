
from rest_framework.serializers import *

from .models import *
from .enums import *


class ActionUsabilitySerializer(Serializer):
    action_type_code = SerializerMethodField()
    uses = SerializerMethodField()

    def get_action_type_code(self, action_type_and_use):
        return action_type_and_use[0].code

    def get_uses(self, action_type_and_use):
        return action_type_and_use[1]


class RoleSerializer(Serializer):
    code = CharField(max_length=Role.CODE_LENGTH)
    name = CharField(max_length=Role.MAX_NAME_LENGTH)
    thumbnail = ReadOnlyField(source='thumbnail_url')
    action_usabilities = ListField(
        child=ActionUsabilitySerializer(),
        source='action_types_and_uses'
    )
    night_immune = BooleanField()
    immune_to_seduction = BooleanField()
    appears_guilty = ReadOnlyField()
    min_in_game = IntegerField()
    max_in_game = ReadOnlyField(source='max_in_game_json')
    win_condition = CharField()
    other_details = CharField()

'''
class PlayerSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    revealed_role = serializers.SerializerMethodField()
    secret_info = serializers.SerializerMethodField()

    def get_username(self, player):
        return player.user.username

    def get_full_name(self, player):
        return player.user.get_full_name()

    def get_status(self, player):
        return PlayerStatus.get_instance(player.status).name

    def get_revealed_role(self, player):
        return (
            Role.get_instance(player.role).name
            if player.role and player.status != PlayerStatus.ALIVE.code
            else None
        )

    def get_secret_info(self, player):
        if player.game.creator != self.context['user']:
            return None
        return {
            'role': _get_role_name(player.role),
            'old_role': _get_role_name(player.old_role),
            'older_role': _get_role_name(player.older_role),
            'actions_used': player.get_actions_used(),
            'doused': player.doused,
            'executioner_target': player.executioner_target,
        }


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, user):
        return user.get_full_name()


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=GAME_NAME_MAX_LENGTH)
    created = serializers.DateField()
    creator = UserSerializer()
    players = serializers.ListField(
        child=PlayerSerializer(),
        source='get_players'
    )
    day_number = serializers.IntegerField()
    is_accepting = serializers.ReadOnlyField()
    user_has_joined = serializers.SerializerMethodField()

    def get_user_has_joined(self, game):
        return game.has_user_playing(self.context['user'])
'''

def _get_role_name(role_code):
    return Role.get_instance(role_code).name if role_code else None
