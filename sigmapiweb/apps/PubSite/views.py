"""
Views for PubSite app.
"""
from django.http import Http404
from django.shortcuts import render
from . import models


def _get_context(page_name):
    """ Returns the context necessary for any public page 
    
    Arguments:
        page_name (str) The url name of the page being rendered
    """
    return {
        'pages': models.PublicPage.displayed_pages(),
        'current_page': models.PublicPage.get_by_url(page_name)
    }


def _get_article_context(page_name):
    """ Returns the context necessary for an article style page 
    
    Arguments:
        page_name (str) The friendly name of the page being rendered
    """
    blocks_dict = {'article_blocks': models.ArticleBlock.blocks_for_page(page_name)}
    blocks_dict.update(_get_context(page_name))
    return blocks_dict


def index(request):
    """
    View for the static index page
    """
    return render(request, 'public/home.html', _get_context('Home'))


def public_page(request, url_name):
    """
    View to reach any public page stored in the database, used as a top-level page
    """
    print('accessed public page --------')
    print('url_name = %s' % url_name)
    page = models.PublicPage.get_by_url(url_name)
    template = None
    if hasattr(page, 'article'):
        template = page.article.template_name()
    elif hasattr(page, 'carouselpage'):
        template = page.carouselpage.template_name()
    if template:
        return render(request, template, _get_context(page.url_name))
    raise Http404('The page "%s" could not be found.' % url_name)


def about(request):
    """
    View for the static chapter history page.
    """
    return render(request, 'public/article.html', _get_article_context('About'))


def activities(request):
    """
    View for the static chapter service page.
    """
    return render(
        request,
        'public/article.html',
        _get_article_context('Service & Activities'),
    )


def donate(request):
    """
    View for the static donate page.
    """
    return render(
        request, 'public/article.html', _get_article_context('Donate'),
    )


def permission_denied(request):
    """
    View for 403 (Permission Denied) error.
    """
    return render(
        request, 'common/403.html', _get_context('Permission Denied'),
    )
