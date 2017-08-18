"""
Views for Links app.
"""
from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from .forms import LinkForm
from .models import Link


@permission_required('Links.access_link', login_url='pub-permission_denied')
def view_all(request):
    """
    Displays all of the links in the system.
    """
    linkform = LinkForm()
    general_links = Link.objects.filter(promoted=False).order_by('-date')
    promoted_links = Link.objects.filter(promoted=True).order_by('-date')
    context = {
        'linkform': linkform,
        'general_links': general_links,
        'promoted_links': promoted_links,
    }
    return render(request, 'links/view.html', context)


@permission_required('Links.add_link', login_url='pub-permission_denied')
def add_link(request):
    """
    Creates a new link to add to the system
    """
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)
            link.poster = request.user
            link.date = datetime.now()

            if not request.user.has_perm('Links.promote_link'):
                link.promoted = False
            link.save()

        return redirect('links-view_all')
    else:
        return redirect('pub-permission_denied')


@permission_required('Links.delete_link', login_url='pub-permission_denied')
def delete_link(request, link):
    """
    Deletes a link.
    """
    if request.method == 'POST':
        try:
            desired_link = Link.objects.get(pk=link)
        except Link.DoesNotExist:
            desired_link = None
        if desired_link:
            try:
                desired_link.delete()
            except PermissionDenied:
                return redirect('pub-permission_denied')
        return redirect('links-view_all')
    else:
        return redirect('pub-permission_denied')
