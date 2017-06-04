
from django.conf.urls import patterns, url

from Mafia.views import *

urlpatterns = patterns('',
    url(r'^$', AboutView.as_view(), name='mafia_about_view'),
    url(r'^roles/$', RolesView.as_view(), name='mafia_roles_view'),
    url(r'^roles/(?P<code>.+)/$', RoleView.as_view(), name='mafia_role_view'),
    url(r'^actiontypes/$', ActionTypesView.as_view(), name='mafia_action_types_view'),
    url(r'^actiontypes/(?P<code>.+)/$', ActionTypeView.as_view(), name='mafia_action_type_view'),
    #url(r'^games/$', GamesView.as_view(), name='mafia_games_view'),
    #url(r'^games/(?P<game_id>[\d]+)/$', GameView.as_view(), name='mafia_game_view'),
    #url(r'^games/(?P<game_id>[\d]+)/players/$', PlayersView.as_view(), name='mafifa_players_view'),
    #url(r'^games/(?P<game_id>[\d]+)/players/(?P<player_username>.*)/$', PlayerView.as_view(), name='mafia_player_view'),
)
