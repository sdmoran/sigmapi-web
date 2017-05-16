
from rest_framework import serializers

from .models import *
from .enums import *


class PlayerSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_username(self, player):
        return player.user.username

    def get_full_name(self, player):
        return player.user.get_full_name()

    def get_role(self, player):
        role_name = (
            Role.get_instance(player.role).name
            if player.role
            else "(Unassigned)"
        )
        return (
            role_name if (
                self.context['user'] == player.game.creator or
                player.status != PlayerStatus.ALIVE.code
            )
            else None
        )

    def get_status(self, player):
        return PlayerStatus.get_instance(player.status).name


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


