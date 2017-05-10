
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import MafiaGame, MafiaPlayer

import mafia

@login_required
def index(request):
    return redirect('Mafia.views.join')

@login_required
def play(request):
    running_games = MafiaGame.objects.exclude(day_number=0).order_by('created')
    running_games.reverse()
    game_infos = []
    for g in running_games:
        players = MafiaPlayer.objects.filter(game=g)
        users = [p.user for p in players]
        joined = request.user in users
        if joined:
            game_infos.append({
                'pk': g.pk,
                'name': g.name,
                'created': g.created,
                'creator_name': g.creator.get_full_name(),
                'status': g.status_string,
            })
    return render(request, 'mafia_home_play.html', {'game_infos': game_infos})

@login_required
def play_game(request, game_id):
    game = _id_to_game(game_id)
    raise Http404('Not implemented.')

@login_required
def join(request):
    inviting_games = MafiaGame.objects.filter(day_number=0).order_by('created')
    inviting_games.reverse()
    game_infos = []
    for g in inviting_games:
        players = MafiaPlayer.objects.filter(game=g)
        users = [p.user for p in players]
        joined = request.user in users
        game_infos.append({
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'creator_name': g.creator.get_full_name(),
            'joined': joined,
        })
    return render(request, 'mafia_home_join.html', {'game_infos': game_infos})

@login_required
def join_game(request, game_id):
    game = _id_to_game(game_id)
    success = mafia.add_player(game, request.user)
    if not success:
        raise Http404('Could not add player to game')
    return redirect('Mafia.views.join')

@login_required
def leave_game(request, game_id):
    game = _id_to_game(game_id)
    success = mafia.remove_player(game, request.user)
    if not success:
        raise Http404('Could not remove player from game')
    return redirect('Mafia.views.join')

@login_required
def spectate(request):
    running_games = MafiaGame.objects.exclude(day_number=0).order_by('created')
    running_games.reverse()
    game_infos = [
        {
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'creator_name': g.creator.get_full_name(),
            'status': g.status_string,
        }
        for g in running_games
    ]
    return render(request, 'mafia_home_spectate.html', {'game_infos': game_infos})

@login_required
def spectate_game(request, game_id):
    game = _id_to_game(game_id)
    raise Http404('Not implemented.')

@login_required
def moderate(request):
    games = MafiaGame.objects.filter(creator=request.user).order_by('created')
    games.reverse()
    game_infos = [
        {
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'status': g.status_string,
        }
        for g in games
    ]
    return render(request, 'mafia_home_moderate.html', {'game_infos': game_infos})

@login_required
def moderate_game(request, game_id):
    game = _id_to_game(game_id)
    raise Http404('Not implemented.')

def _id_to_game(game_id):
    try:
        return MafiaGame.objects.get(pk=game_id)
    except MafiaGame.DoesNotExist:
        raise Http404('Invalid game ID: ' + game_id2)

