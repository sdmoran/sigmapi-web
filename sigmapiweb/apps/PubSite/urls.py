from django.conf.urls import url, include
from django.contrib.auth import views as dsl

from . import views

urlpatterns = [
    url(r'^login', dsl.login, name='pub-login'),
    url(r'^logout', dsl.logout_then_login, name='pub-logout'),
    url(r'^$', views.index, name='pub-index'),
    url(r'^history[/]$', views.history, name='pub-history'),
    url(r'^service[/]$', views.service, name='pub-service'),
    url(r'^403/', views.permission_denied, name='pub-permission_denied'),
    url(r'^donate/', views.donate, name='pub-donate')
]
