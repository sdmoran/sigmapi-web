from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^article/$',
        view=views.create_article,
        name='create-article',
    ),
]
