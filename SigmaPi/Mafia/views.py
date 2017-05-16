
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
        serializer = GameSerializer(games, many=True, context={'user': request.user})
        return Response(serializer.data)
