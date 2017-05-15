
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'Mafia.views.index'),
    url(r'^play/$', 'Mafia.views.play'),
    url(r'^play/(?P<game_id>[\d]+)/$', 'Mafia.views.play_game'),
    url(r'^join/$', 'Mafia.views.join'),
    url(r'^join-game/(?P<game_id>[\d]+)/$', 'Mafia.views.join_game'),
    url(r'^leave-game/(?P<game_id>[\d]+)/$', 'Mafia.views.leave_game'),
    url(r'^spectate/$', 'Mafia.views.spectate'),
    url(r'^spectate/(?P<game_id>[\d]+)/$', 'Mafia.views.spectate_game'),
    url(r'^moderate/$', 'Mafia.views.moderate'),
    url(r'^moderate/(?P<game_id>[\d]+)/$', 'Mafia.views.moderate_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/add/$', 'Mafia.views.add_user_to_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/remove/$', 'Mafia.views.remove_user_from_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/assign/$', 'Mafia.views.assign_role'),
    url(r'^add/$', 'Mafia.views.add_game'),
)
