import warnings

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from apps.UserInfo import urls as userinfo_urls
from apps.Secure import urls as secure_urls
from apps.PubSite import urls as public_urls


admin.autodiscover()

# Turns deprecation warnings into errors
warnings.simplefilter('error', DeprecationWarning)

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(userinfo_urls)),
    url(r'^secure/', include(secure_urls)),
    url(r'^', include(public_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
