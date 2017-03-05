
from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='Mafia.views.index')),
    url(r'^all/$', 'Mafia.views.index'),
)
