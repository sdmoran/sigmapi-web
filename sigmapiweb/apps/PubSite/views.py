"""
Views for PubSite app.
"""
from django.conf import settings
from django.shortcuts import render
from models import ArticleBlock


def _get_context(page_name):
    """ Returns the context necessary for any public page 
    
    Arguments:
        page_name (str) The friendly name of the page being rendered
    """
    return {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': page_name
    }


def _get_article_context(page_name):
    """ Returns the context necessary for an article style page 
    
    Arguments:
        page_name (str) The friendly name of the page being rendered
    """
    blocks_dict = {'article_blocks': ArticleBlock.blocks_for_page(page_name)}
    blocks_dict.update(_get_context(page_name))
    return blocks_dict


def index(request):
    """
    View for the static index page
    """
    return render(request, 'public/home.html', _get_context('Home'))


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
