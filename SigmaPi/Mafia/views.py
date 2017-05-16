
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import mafia
from .models import *
from .errors import *
from .serializers import *


class GamesView(APIView):

    permissions = (permissions.IsAuthenticated,)

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={
            'user': request.user
        })
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
        serializer = GameSerializer(game, context={
            'user': request.user
        })
        return OkResponse(serializer.data)


class OkResponse(Response):
    status_code = 200


class BadRequestResponse(Response):
    status_code = 400
