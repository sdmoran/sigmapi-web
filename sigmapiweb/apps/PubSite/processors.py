"""
Custom Django Context Processors
"""
from django.conf import settings


def menu_items(request):
    """
    Adds the main navigation menu items to the django template context
    """
    return {'PUBLIC_LINKS': settings.PUBLIC_PAGES}
