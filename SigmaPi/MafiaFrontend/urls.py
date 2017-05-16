
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'MafiaFrontend.views.index'),
    url(r'^play/$', 'MafiaFrontend.views.play'),
    url(r'^play/(?P<game_id>[\d]+)/$', 'MafiaFrontend.views.play_game'),
    url(r'^join/$', 'MafiaFrontend.views.join'),
    url(r'^join-game/(?P<game_id>[\d]+)/$', 'MafiaFrontend.views.join_game'),
    url(r'^leave-game/(?P<game_id>[\d]+)/$', 'MafiaFrontend.views.leave_game'),
    url(r'^spectate/$', 'MafiaFrontend.views.spectate'),
    url(r'^spectate/(?P<game_id>[\d]+)/$', 'MafiaFrontend.views.spectate_game'),
    url(r'^moderate/$', 'MafiaFrontend.views.moderate'),
    url(r'^moderate/(?P<game_id>[\d]+)/$', 'MafiaFrontend.views.moderate_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/add/$', 'MafiaFrontend.views.add_user_to_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/remove/$', 'MafiaFrontend.views.remove_user_from_game'),
    url(r'^moderate/(?P<game_id>[\d]+)/assign/$', 'MafiaFrontend.views.assign_role'),
    url(r'^add/$', 'MafiaFrontend.views.add_game'),
)
