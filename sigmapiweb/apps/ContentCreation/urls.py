from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^article/$',
        view=views.create_article,
        name='create-article',
    ),
    url(
        regex=r'^article_block/$',
        view=views.create_article_block,
        name='create-article-block'
    ),
    url(
        regex=r'^public_image/$',
        view=views.create_public_image,
        name='create-public-image'
    ),
     url(
        regex=r'^carousel_slide/$',
        view=views.create_carousel_slide,
        name='create-carousel-slide'
    ),
]
