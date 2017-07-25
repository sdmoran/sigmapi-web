from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.users, name='userinfo-users'),
    url(r'^password/', views.change_password, name='userinfo-change_password'),
]
