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
    )
]
