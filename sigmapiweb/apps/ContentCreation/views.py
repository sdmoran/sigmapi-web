from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from . import forms
from apps.PubSite import models


@login_required
def create_article(request):
    """
    View to submit a form to create an article on the PubSite
    """
    if request.method == 'POST':
        article_form = forms.ArticleForm(request.POST)

        if article_form.is_valid():
            friendly_name = article_form.cleaned_data['friendly_name']
            url_name = article_form.cleaned_data['url_name']
            background_img = article_form.cleaned_data['background_img']
            article = models.Article.objects.create(
                friendly_name=friendly_name,
                url_name=url_name,
                background_img=background_img,
            )
            article.save()
    else:
        article_form = forms.ArticleForm()
    return render(request, 'author/create_article.html', {'form': article_form})

def create_article_block(request):
    """
    View to submit a form to create an article block on the Pubsite
    """
    if request.method == 'POST':
        article_block_form = forms.ArticleBlockForm(request.POST)

        if article_block_form.is_valid():
            page = article_block_form.cleaned_data['page']
            title = article_block_form.cleaned_data['title']
            anchor_id = article_block_form.cleaned_data['anchor_id']
            body = article_block_form.cleaned_data['body']
            article_block = models.ArticleBlock.objects.create(
                page=page,
                title=title,
                anchor_id=anchor_id,
                body=body,
            )
            article_block.save()
    else:
        article_block_form = forms.ArticleBlockForm()
    return render(request, 'author/create_article_block.html',{'form' : article_block_form})