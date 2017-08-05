from django.conf.urls import include, url

from Secure import views


urlpatterns = [
    url(r'^$', views.index, name='secure-index'),
    url(r'^archives/', include('Archive.urls')),
    url(r'^parties/', include('PartyList.urls')),
    url(r'^users/', include('UserInfo.secure_urls')),
    url(r'^links/', include('Links.urls')),
    url(r'^standards/', include('Standards.urls')),
    url(r'^scholarship/', include('Scholarship.urls'))
]
