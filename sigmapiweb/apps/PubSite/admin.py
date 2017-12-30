"""
Admin config for PubSite app.
"""
from common.utils import register_model_admins

from . import models


register_model_admins(
    models.ArticleBlock,
    models.PublicPage,
    models.Article,
    models.CarouselSlide,
    models.PublicImage,
    models.CarouselPage
)
