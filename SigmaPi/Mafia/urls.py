
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'Mafia.views.index'),
    url(r'^play/$', 'Mafia.views.play'),
    url(r'^join/$', 'Mafia.views.join'),
    url(r'^spectate/$', 'Mafia.views.spectate'),
    url(r'^moderate/$', 'Mafia.views.moderate'),
    url(r'^join/(?P<game_id>[\d]+)/$', 'Mafia.views.join_game'),
    url(r'^leave/(?P<game_id>[\d]+)/$', 'Mafia.views.leave_game'),
)
