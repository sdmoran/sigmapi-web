from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'UserInfo.views.users'),
    url(r'^password/', 'UserInfo.views.change_password'),
)