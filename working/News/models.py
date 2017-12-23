"""
Models for News app.
"""
from django.db import models
from django.contrib.auth.models import User

from common.mixins import ModelMixin


def news_item_body_path(news_item, filename):
    """
    TODO: Docstring
    """
    return 'news-items/{0}/{1}'.format(news_item.key, filename)


def featured_item_image_path(featured_item, filename):
    """
    TODO: Docstring
    """
    return 'featured-items/{0}/{1}'.format(featured_item.key, filename)


class NewsItem(ModelMixin, models.Model):
    """
    TODO: Docstring
    """
    key = models.CharField(unique=True, max_length=16)
    title = models.CharField(max_length=70)
    date_posted = models.DateField()
    body_file = models.FileField(upload_to=news_item_body_path)
    visible = models.BooleanField(default=False)


class FeaturedItem(ModelMixin, models.Model):
    """
    TODO: Docstring
    """
    key = models.CharField(unique=True, max_length=16)
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=140)
    image = models.FileField(upload_to=featured_news_item_image_path)
    link = models.TextField()
    index = models.IntegerField()
    visible = models.BooleanField(default=False)
