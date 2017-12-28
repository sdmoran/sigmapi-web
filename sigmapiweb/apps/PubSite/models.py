"""
Models for the Public Site
"""

from django.db import models

from common.mixins import ModelMixin
from common.settings.base import PUBLIC_PAGES


class ArticleBlock(ModelMixin, models.Model):
    """
    Model for a block of article text on the PubSite
    """
    page = models.CharField(max_length=200, choices=[[name, name] for name in PUBLIC_PAGES.iterkeys()])
    anchor_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    precedence = models.IntegerField(default=0)
    valid = models.BooleanField()

    @staticmethod
    def blocks_for_page(page):
        """
        The valid article blocks for the given page in order of -precedence
        
        Arguments:
            page (str) The friendly-name of the page in which the block resides
        """
        return ArticleBlock.objects.filter(valid=True, page=page).order_by('-precedence')
