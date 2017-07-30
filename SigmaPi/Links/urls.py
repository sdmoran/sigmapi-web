from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = patterns('',
    url(r'^$', 'Links.views.view_all'),
    url(r'^add/$', 'Links.views.add_link'),
    url(r'^(?P<link>[\d]+)/delete/$', 'Links.views.delete_link')
)
