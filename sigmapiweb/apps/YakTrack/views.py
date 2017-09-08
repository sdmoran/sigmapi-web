""" Views for the YakTrack App """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


@login_required
def index(request):
    """ Displays YakTrack main view """


