
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, user):
        return user.get_full_name()


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=GAME_NAME_MAX_LENGTH)
    players = serializers.ListField(
        child=UserSerializer(),
        source='get_playing_users'
    )
    day_number = serializers.IntegerField()
    user_has_joined = serializers.SerializerMethodField()

    def get_user_has_joined(self, game):
        return game.has_user_playing(self.context['user'])
