"""
Root URLs for project.
"""
import warnings

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from apps.PubSite import urls as public_urls
from apps.Secure import urls as secure_urls
from apps.UserInfo import urls as userinfo_urls
import private_storage.urls


admin.autodiscover()

# Turns deprecation warnings into errors
warnings.simplefilter('error', DeprecationWarning)

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(
        regex=r'^admin/',
        view=admin.site.urls,
    ),
    url(
        regex=r'^brothers/',
        view=include(userinfo_urls),
    ),
    url(
        regex=r'^users/',
        view=include(userinfo_urls),
    ),
    url(
        regex=r'^secure/',
        view=include(secure_urls),
    ),
    url(
        regex=r'^',
        view=include(public_urls),
    ),
    url('^auth-required/', include(private_storage.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
