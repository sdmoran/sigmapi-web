
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import MafiaGame

@login_required
def index(request):
    """
        View for all mafia games
    """
    games = MafiaGame.objects.all()
    return render(request, 'mafia-home.html', {})
