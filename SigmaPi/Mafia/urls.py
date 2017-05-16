
from django.conf.urls import patterns, url

from Mafia.views import *

urlpatterns = patterns('',
    url(r'^games/$', GamesView.as_view()),
)
