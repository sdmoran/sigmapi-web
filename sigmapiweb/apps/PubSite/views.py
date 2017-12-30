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


def public_page(request, url_name):
    """
    View to reach any public page stored in the database, used as a top-level page
    """
    page = models.PublicPage.get_by_url(url_name)
    template = None
    if hasattr(page, 'article'):
        template = page.article.template_name()
    elif hasattr(page, 'carouselpage'):
        template = page.carouselpage.template_name()
    if template:
        return render(request, template, _get_context(page.url_name))
    raise Http404('The page "%s" could not be found.' % url_name)


def index(request):
    """
    View for the static index page
    """
    return public_page(request, 'home')


def permission_denied(request):
    """
    View for 403 (Permission Denied) error.
    """
    return render(
        request, 'common/403.html', _get_context('Permission Denied'),
    )
