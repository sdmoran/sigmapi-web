"""
URLs for Secure app.
"""
from django.conf.urls import include, url

from apps.Archive import urls as archive_urls
from apps.PartyList import urls as parties_urls
from apps.UserInfo import secure_urls as userinfo_urls
from apps.Links import urls as links_urls
from apps.Standards import urls as standards_urls
from apps.Scholarship import urls as scholarship_urls
from apps.ContentCreation import urls as content_creation_urls

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='secure-index',
    ),
    url(
        regex=r'^archives/',
        view=include(archive_urls),
    ),
    url(
        regex=r'^parties/',
        view=include(parties_urls),
    ),
    url(
        regex=r'^users/',
        view=include(userinfo_urls),
    ),
    url(
        regex=r'^links/',
        view=include(links_urls),
    ),
    url(
        regex=r'^standards/',
        view=include(standards_urls),
    ),
    url(
        regex=r'^scholarship/',
        view=include(scholarship_urls),
    ),
    url(
        regex=r'^author/',
        view=include(content_creation_urls)
    )
]
