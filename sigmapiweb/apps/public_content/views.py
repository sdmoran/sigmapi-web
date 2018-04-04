# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django_downloadview import sendfile

# Create your views here.

@login_required
@require_GET
def index(_request):
    """
    TODO: Docstring
    """
    return redirect('public-content-article')

@login_required
@require_GET
def article(request):
    """
    TODO: Docstring
    """

    return render(request, 'scholarship/resources.html',)