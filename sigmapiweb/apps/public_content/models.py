# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from sigmapiweb.apps.PubSite.models import ArticleBlock, CarouselSlide, Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['friendly_name', 'url_name', 'background_img']


class ArticleBlockForm(ModelForm):
    class Meta:
        model = ArticleBlock
        fields = ['page', 'anchor_id', 'title', 'body', 'precedence']


class CarouselSlideForm(ModelForm):
    class Meta:
        model = CarouselSlide
        fields = ['image', 'title', 'description', 'precedence']
