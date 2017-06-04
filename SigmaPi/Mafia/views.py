
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import mafia
from .models import *
from .errors import *
from .serializers import *


class AuthAPIView(APIView):
    permissions = (permissions.IsAuthenticated,)


_ABOUT_STR = '''TODO write about string
'''

class AboutView(APIView):

    def get(self, request):
        return OkResponse({
            'about': _ABOUT_STR,
            'version': '0.1',
            'documentation_url': (
                'https://github.com/kdmccormick/sigmapi-web/blob/' +
                'rest-and-relaxation/docs/api/Mafia/v0/Mafia_v0.md'
            ),
        })


class ChoiceEnumerationAllView(AuthAPIView):

    def get(self, request):
        instances = self.enumeration.get_instances()
        data = {
            instance.code: self.serializer(instance).data
            for instance in instances
        }
        return OkResponse(data)


class ChoiceEnumerationSingleView(AuthAPIView):

    def get(self, request, code):
        instance = self.enumeration.get_instance(code)
        if instance:
            serializer = self.serializer(instance)
            return OkResponse(serializer.data)
        else:
            raise Http404(
                self.enumeration.__name__ + ' code \'' + code + '\' is invalid.'
            )
    

class RolesView(ChoiceEnumerationAllView):
    enumeration = Role
    serializer = RoleSerializer


class RoleView(ChoiceEnumerationSingleView):
    enumeration = Role
    serializer = RoleSerializer


class ActionTypesView(ChoiceEnumerationAllView):
    enumeration = ActionType
    serializer = ActionTypeSerializer


class ActionTypeView(ChoiceEnumerationSingleView):
    enumeration = ActionType
    serializer = ActionTypeSerializer


'''
class GamesView(AuthAPIView):

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(
            games, many=True, context={'user': request.user}
        )
        return OkResponse(serializer.data)

    def post(self, request):
        name = request.data.get('name', None)
        if name is None:
            return BadRequestResponse('Expected value for \'name\'')
        if not (1 <= len(name) <= GAME_NAME_MAX_LENGTH):
            return BadRequestResponse(
                'Length of game name must be between 1 and ' +
                `GAME_NAME_MAX_LENGTH`
            )
        game = Game.create_game(request.user, request.data['name'])
        serializer = GameSerializer(game, context={'user': request.user})
        return CreatedResponse(
            serializer.data,
            reverse('mafia_game_view', args=(game.pk,))
        )


class GameView(APIView):

    def get(self, request, game_id):
        game = _get_game(game_id)
        serializer = GameSerializer(game, context={'user': request.user})
        return OkResponse(serializer.data)

    def delete(self, request, game_id):
        game = _get_game(game_id)
        if not (request.user.is_staff or request.user == game.creator):
            return PermissionDeniedResponse(
                'To delete a game you must be the game\'s creator, or staff.'
            )
        if game.is_finished:
            return BadRequestResponse(
                'Cannot delete a finished game.'
            )
        game.delete()
        return NoContentResponse()


class PlayersView(APIView):

    def get(self, request, game_id):
        game = _get_game(game_id)
        serializer = PlayerSerializer(
            game.get_players(), many=True, context={'user': request.user}
        )
        return OkResponse(serializer.data)

    def post(self, request, game_id):
        username = request.data.get('username', None)
        if not username:
            return BadRequestResponse('Expected value for \'username\'.')
        return _add_player(request, game_id, username)
        

class PlayerView(APIView):

    def get(self, request, game_id, player_username):
        game = _get_game(game_id)
        user = _get_user(player_username)
        try:
            player = Player.get(game=game, user=user)
        except Player.DoesNotExist:
            raise Http404(
                'User ' + player_username + 
                ' is not a player in game with ID ' + game_id + '.'
            )
        serializer = PlayerSerializer(player, context={'user': request.user})
        return OkResponse(serializer.data)

    def put(self, request, game_id, player_username):
        return _add_player(request, game_id, player_username)

'''

class OkResponse(Response):
    status_code = 200


class CreatedResponse(Response):
    status_code = 201

    def __init__(self, payload, location, *args, **kwargs):
        super(CreatedResponse, self).__init__(payload, *args, **kwargs)
        self['Location'] = location


class NoContentResponse(Response):
    status_code = 204


class BadRequestResponse(Response):
    status_code = 400


class PermissionDeniedResponse(Response):
    status_code = 403


def _add_player(request, game_id, username):
    game = _get_game(game_id)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return BadRequestResponse(
            'User \'' + username + '\' does not exist'
        )
    try:
        player = game.add_player(user)
    except MafiaUserError as e:
        return BadRequestResponse(e.message)
    serializer = PlayerSerializer(player, context={'user': request.user})
    return CreatedResponse(
        serializer.data,
        reverse('mafia_player_view', args=(game_id, player.user.username))
    )


def _get_game(game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404(
            'Game with ID ' + game_id + ' does not exist.'
        )
    else:
        return game

def _get_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(
            'User \'' + username + '\' does not exist.'
        )
    else:
        return user

