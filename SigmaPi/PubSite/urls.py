from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^logout', 'django.contrib.auth.views.logout_then_login'),
	url(r'^$', 'PubSite.views.index'),
	url(r'^history[/]$', 'PubSite.views.history'),
	url(r'^service[/]$', 'PubSite.views.service'),
	url(r'^403/', 'PubSite.views.permission_denied'),
	url(r'^donate/', 'PubSite.views.donate')
)