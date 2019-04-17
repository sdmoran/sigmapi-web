"""
URLs for Slack App Endpoints
"""

from django.conf.urls import url
from . import api

urlpatterns = [
    url(
        regex=r'^sigma-poll/create/$',
        view=api.sigma_poll_create,
        name='slack_sigma-poll-create'
    ),
    url(
        regex=r'^sigma-poll/update/$',
        view=api.sigma_poll_update,
        name='slack_sigma-poll-update'
    ),
    url(
        regex=r'^clique/create/$',
        view=api.clique_create,
        name='slack_clique-create'
    ),
    url(
        regex=r'^clique/send/$',
        view=api.clique_send_msg,
        name='slack_clique-send'
    ),
    url(
        regex=r'^clique/add_users/$',
        view=api.clique_add_users,
        name='slack_clique-add-users'
    ),
    url(
        regex=r'^clique/remove_users/$',
        view=api.clique_remove_users,
        name='slack_clique-remove-users'
    ),
    url(
        regex=r'^clique/delete/$',
        view=api.clique_delete,
        name='slack_clique-delete'
    ),
    url(
        regex=r'^clique/list/$',
        view=api.clique_list,
        name='slack_clique-list'
    ),
]
