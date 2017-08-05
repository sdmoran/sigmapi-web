from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static 

from . import views


urlpatterns = [
    url(r'^$', views.view_all, name='links-view_all'),
    url(r'^add/$', views.add_link, name='links-add_link'),
    url(r'^(?P<link>[\d]+)/delete/$', views.delete_link, name='links-delete_link')
]
