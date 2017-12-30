"""
Models for the Public Site
"""

from django.db import models
from django.shortcuts import get_object_or_404

from common.mixins import ModelMixin


class PublicImage(ModelMixin, models.Model):
    """ Model representing an image's path on the filesystem """
    path = models.CharField(max_length=200)

    def __str__(self):
        return str(self.path)


class PublicPage(ModelMixin, models.Model):
    """
    Superclass for any public page which has a name and should have a labeled tab in the NavBar
    """
    friendly_name = models.CharField(max_length=50)
    url_name = models.CharField(max_length=50, unique=True)
    valid = models.BooleanField(default=False)
    precedence = models.IntegerField(default=0)

    def __str__(self):
        return self.friendly_name

    @property
    def relative_url(self):
        """
        A (slightly hacky) way to get the relative url since we know pages are top-level
        Could maybe replace with a reverse() call.
        """
        return '/%s' % str(self.url_name)

    class Meta:
        ordering = ['-precedence']

    @staticmethod
    def displayed_pages():
        """ Returns all valid pages ordered by precedence """
        return PublicPage.objects.filter(valid=True)

    @staticmethod
    def all_pages():
        """ Returns all pages, including those which are invalid """
        return PublicPage.objects.all()

    @staticmethod
    def invalid_pages():
        """ Returns pages which are not considered valid """
        return PublicPage.objects.filter(valid=False)

    @staticmethod
    def get_by_name(name):
        """
        Returns the page for the given friendly name, or 404 if does not exist
        
        Arguments:
            name (str)
        """
        return get_object_or_404(PublicPage, friendly_name=name)

    @staticmethod
    def get_by_url(url):
        """
        Returns the page for the given url name, or 404 if does not exist

        Arguments:
            url (str)
        """
        print('getting object for url %s' % url)
        return get_object_or_404(PublicPage, url_name=url)

    @staticmethod
    def template_name():
        """ 
        Method which should be overridden by subclasses returning the name of the template associated
        with the page. Note the class is not abstract, although it cannot be rendered. This is because
        it actually needs to be instantiated in order to query PublicPages. At the database level, its
        subclasses are independent tables which Django automatically JOIN's during queries.
        """
        return None


class Article(PublicPage):
    """
    Model for an article on the public site
    """
    background_img = models.ForeignKey(PublicImage, null=True, on_delete=models.SET_NULL)

    @property
    def valid_blocks(self):
        """ Return the valid ArticleBlock's associated with this Article """
        return self.article_blocks.filter(valid=True)

    @property
    def all_blocks(self):
        """ Return all ArticleBlock's associated with this Article """
        return self.article_blocks.all()

    @staticmethod
    def template_name():
        """ Returns the name of the template associated with this model """
        return 'public/article.html'


class ArticleBlock(ModelMixin, models.Model):
    """
    Model for a block of article text on the PubSite
    """
    page = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_blocks')
    anchor_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    precedence = models.IntegerField(default=0)
    valid = models.BooleanField()

    class Meta:
        ordering = ['-precedence']

    @staticmethod
    def blocks_for_page(page):
        """
        The valid article blocks for the given page in order of -precedence

        Arguments:
            page (str) The friendly-name of the page in which the block resides
        """
        return ArticleBlock.objects.filter(valid=True, page=page)


class CarouselSlide(ModelMixin, models.Model):
    """
    Model representing a slide in an image carousel
    """
    image = models.ForeignKey(PublicImage)
    title = models.TextField()
    description = models.TextField()
    precedence = models.IntegerField()

    class Meta:
        ordering = ['-precedence']


class CarouselPage(PublicPage):
    """
    Model for an image-carousel-style page
    """
    slides = models.ManyToManyField(CarouselSlide)

    @staticmethod
    def template_name():
        return 'public/carousel.html'

