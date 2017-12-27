"""
Models for the Public Site
"""

from django.db import models


class PubPage(models.Model):
    """
    Model for a page on the PubSite which contains ArticleBlocks
    """
    name = models.CharField(max_length=200)
    background_img_name = models.CharField(max_length=200)
    valid = models.BooleanField()

    @property
    def article_blocks(self):
        """
        The blocks belonging to this article

        :return: QuerySet of the valid articles which belong in this page in order of precedence 
        """
        return self.articles.filter(valid=True).order_by('-precedence')

    @staticmethod
    def all_valid_pages():
        """
        Fetches all the pages which should be displayed on the PubSite

        :return: QuerySet of all pages which are valid
        """
        return PubPage.objects.filter(valid=True)


class ArticleBlock(models.Model):
    """
    Model for a block of article text on the PubSite
    """
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    page = models.ForeignKey(PubPage, related_name='articles', on_delete=models.CASCADE)
    precedence = models.IntegerField(default=0)
    valid = models.BooleanField()
