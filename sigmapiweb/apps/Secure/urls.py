from django.conf.urls import include, url

from apps.Archive import urls as archive_urls
from apps.PartyList import urls as parties_urls
from apps.UserInfo import secure_urls as userinfo_urls
from apps.Links import urls as links_urls
from apps.Standards import urls as standards_urls
from apps.Scholarship import urls as scholarship_urls

from . import views


urlpatterns = [
    url(r'^$', views.index, name='secure-index'),
    url(r'^archives/', include(archive_urls)),
    url(r'^parties/', include(parties_urls)),
    url(r'^users/', include(userinfo_urls)),
    url(r'^links/', include(links_urls)),
    url(r'^standards/', include(standards_urls)),
    url(r'^scholarship/', include(scholarship_urls))
]
