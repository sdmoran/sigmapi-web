from django.forms import ModelForm
from apps.PubSite.models import Article, ArticleBlock, PublicImage, CarouselSlide


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['friendly_name', 'url_name', 'background_img']


class ArticleBlockForm(ModelForm):
    class Meta:
        model = ArticleBlock
        fields = ['page', 'title', 'anchor_id', 'body']


class PublicImageForm(ModelForm):
    class Meta:
        model = PublicImage
        fields = ['path']


class CarouselSlideForm(ModelForm):
    class Meta:
        model = CarouselSlide
        fields = ['image', 'title', 'description', 'precedence']

