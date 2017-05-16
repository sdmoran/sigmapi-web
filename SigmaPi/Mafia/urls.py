
from django.conf.urls import patterns, url

from Mafia.views import *

urlpatterns = patterns('',
    url(r'^games/$', GamesView.as_view()),
    url(r'^games/(?P<game_id>[\d]+)/$', GameView.as_view()),
)
