from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^article/$',
        view=views.create_article,
        name='create-article',
    ),
    url(
        regex=r'^article_block',
        view=views.create_article_block,
        name='create-article-block'
    )
]