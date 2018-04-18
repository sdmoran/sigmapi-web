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
