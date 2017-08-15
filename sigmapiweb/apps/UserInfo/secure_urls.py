from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^$', views.manage_users, name='userinfo-manage_users'),
    url(r'^add/', views.add_users, name='userinfo-add_users'),
    url(r'^edit/(?P<user>\w+)/$', views.edit_user, name='userinfo-edit_user'),
    url(r'^reset_password/(?P<user>\w+)/$', views.reset_password, name='userinfo-reset_password'),
]
