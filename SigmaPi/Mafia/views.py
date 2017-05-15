
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import MafiaGame, MafiaPlayer
from .forms import MafiaAddGameForm, MafiaAddUserToGameForm

import mafia

@login_required
def index(request):
    return redirect('Mafia.views.play')


##############################################
# Playing
##############################################

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
    return render(request, 'mafia_play.html', {'game_infos': game_infos})

@login_required
def play_game(request, game_id):
    game = _id_to_game(game_id)
    return _not_implemented()


##############################################
# Joining/Leaving
##############################################

@login_required
def join(request):
    accepting_games = MafiaGame.objects.filter(day_number=0).order_by('created')
    accepting_games.reverse()
    game_infos = []
    for g in accepting_games:
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
    return render(request, 'mafia_join.html', {'game_infos': game_infos})

@login_required
def join_game(request, game_id):
    game = _id_to_game(game_id)
    return _do_and_redirect(
        fn=mafia.add_user,
        fn_args=(game, request.user,),
        redirect_to='Mafia.views.join',
    )

@login_required
def leave_game(request, game_id):
    game = _id_to_game(game_id)
    return _do_and_redirect(
        fn=mafia.remove_user,
        fn_args=(game, request.user,),
        redirect_to='Mafia.views.join',
    )


##############################################
# Spectating
##############################################

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
    return render(request, 'mafia_spectate.html', {'game_infos': game_infos})

@login_required
def spectate_game(request, game_id):
    game = _id_to_game(game_id)
    return _not_implemented()


##############################################
# Moderating
##############################################

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
    return render(request, 'mafia_moderate.html', {'game_infos': game_infos})

@login_required
def moderate_game(request, game_id):
    game = _id_to_game(game_id)
    _check_creator(request, game)
    if game.is_accepting:
        players = MafiaPlayer.objects.filter(game=game)
        signed_up_users = [
            (p.user.get_full_name(), p.user.username)
            for p in players
        ]
        add_user_form = MafiaAddUserToGameForm(game)
        return render(request, 'mafia_moderate_game_accepting.html', {
            'game': game,
            'signed_up_users': signed_up_users,
            'add_user_form': add_user_form,
        })
    else:
        return _not_implemented()

@login_required
def add_game(request):
    if request.method == 'POST':
        form = MafiaAddGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            game = MafiaGame(name=name, created=datetime.now(), creator=request.user)
            game.save()
            return redirect('Mafia.views.moderate')
        else:
            return render(request, 'mafia_add_game.html', {'form': form})
    else:
        form = MafiaAddGameForm()
        return render(request, 'mafia_add_game.html', {'form': form})

@login_required
def add_user_to_game(request, game_id, username=None):
    game = _id_to_game(game_id)
    _check_creator(request, game)
    if request.method == 'POST':
        form = MafiaAddUserToGameForm(None, request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
        else:
            return redirect('Mafia.views.moderate_game', args=(game_id,))
    elif username:
        user = _username_to_user(username)
    else:
        return HttpResponse('''
            <h1>400: Bad Request</h1>
            <h3>Expected username either in URL or in POST data</h3>
        ''', status=400)
    return _do_and_redirect(
        fn=mafia.add_user,
        fn_args=(game, user),
        redirect_to='Mafia.views.moderate_game',
        game_id=game_id,
    )

@login_required
def remove_user_from_game(request, game_id, username):
    game = _id_to_game(game_id)
    _check_creator(request, game)
    user = _username_to_user(username)
    return _do_and_redirect(
        fn=mafia.remove_user,
        fn_args=(game, user),
        redirect_to='Mafia.views.moderate_game',
        game_id=game_id,
    )


##############################################
# Utilities
##############################################

def _id_to_game(game_id):
    try:
        return MafiaGame.objects.get(pk=game_id)
    except MafiaGame.DoesNotExist:
        raise Http404('Invalid game ID: ' + game_id2)

def _username_to_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('Invalid username: ' + username)

def _do_and_redirect(fn, fn_args, redirect_to, **redirect_kwargs):
    try:
        fn(*fn_args)
    except MafiaUserError as e:
        raise Http404(e.message)
    except MafiaError as e:
        return _server_error(e)
    return redirect(reverse(redirect_to, kwargs=redirect_kwargs))

def _server_error(error):
    print 'INTERNAL MAFIA ERROR: ' + `err`
    return HttpResponseServerError('''
        <h1>500: Internal server error</h1>
        <h3>Please contact the webmaster</h3>
    ''')

def _not_implemented():
    return HttpResponse('''
        <h1>501: Not implemented</h1>
        <h3>Please contact the webmaster</h3>
    ''', status=501)

def _check_creator(request, game):
    if game.creator != request.user:
        raise PermissionDenied()
