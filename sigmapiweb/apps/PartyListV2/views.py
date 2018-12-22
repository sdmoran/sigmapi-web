from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django_downloadview import sendfile
from django.views.decorators.http import require_GET, require_POST
import os

from apps.PartyListV2.forms import EditPartyForm, RestrictedGuestForm
from apps.PartyListV2.models import Party, RestrictedGuest

import apps.PartyList.models


@login_required
@permission_required("PartyListV2.view_parties")
def index(request):
    parties = Party.objects.all().order_by("party_start")
    old_parties = apps.PartyList.models.Party.objects.all().order_by("date")
    context = {
        'all_parties': parties,
        'old_parties': old_parties
    }
    return render(request, 'partiesv2/all.html', context)


@login_required
@permission_required("PartyListV2.view_parties")
def guests(request, party_id):
    try:
        requested_party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return redirect("partylist-index")

    brothers = [
        (user.username, user.get_full_name())
        for user in
        User.objects.filter(
            groups__name__in=['Brothers', 'Pledges']
        ).order_by('first_name')
    ]
    context = {
        'party': requested_party,
        'brothers': brothers,
    }
    return render(request, 'partiesv2/guests.html', context)


@login_required
@permission_required(
    'PartyListV2.manage_parties',
    login_url='pub-permission_denied'
)
def delete_party(request, party_id):
    """
        Deletes the party with the ID that is sent in the post request
        """
    if request.method == 'POST':
        try:
            party = Party.objects.get(pk=party_id)
        except Party.DoesNotExist:
            pass
        else:
            party.delete()
    return redirect("partylist-manage_parties")

@login_required
@permission_required(
    'PartyListV2.manage_parties',
    login_url='pub-permission_denied'
)
def edit_party(request, party_id):

    try:
        requested_party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return redirect("partylist-manage_parties")

    messages = []
    error_messages = []
    if request.method == 'POST':
        # If this is a POST request, the form has been submitted
        form = EditPartyForm(request.POST, request.FILES,
                             instance=requested_party)

        if form.is_valid():  # Check that form is valid
            requested_party = form.save()
            messages.append(requested_party.name + " saved.")
        else:
            error_messages.append("Error editing party.")
    else:
        form = EditPartyForm(instance=requested_party)

    context = {
        'adding_new': False,
        'form': form,
        'requested_party': requested_party,
        'errors': form.errors,
        'message': messages,
        'error_messages': error_messages
    }

    return render(request, 'partiesv2/edit.html', context)


@login_required
@permission_required(
    'PartyListV2.manage_parties',
    login_url='pub-permission_denied'
)
def manage_parties(request):
    all_parties = Party.objects.all().order_by("party_start")
    context = {
        'all_parties': all_parties,
    }
    return render(request, 'partiesv2/manage.html', context)


@login_required
@permission_required(
    'PartyListV2.manage_parties',
    login_url='pub-permission_denied'
)
@require_POST
def add_party(request):

    context = {
        'message': [],
        'adding_new': True,
        'form': EditPartyForm()
    }

    form = EditPartyForm(request.POST, request.FILES)
    if form.is_valid():
        party = form.save()
        context['message'].append(party.name + " successfully added.")
    else:
        context['message'].append("Error adding party.")

    return render(request, 'partiesv2/edit.html', context)



def remove_graylisting(request, gl_id):
    guest = RestrictedGuest.objects.get(pk=gl_id, graylisted=True)

    if guest.can_be_deleted_by(request.user):
        guest.delete()

    return HttpResponseRedirect(reverse(restricted_lists))


def remove_blacklisting(request, bl_id):
    guest = RestrictedGuest.objects.get(pk=bl_id, graylisted=False)

    if guest.can_be_deleted_by(request.user):
        guest.delete()

    return HttpResponseRedirect(reverse(restricted_lists))


def manage_restricted_lists(request):
    return None

@permission_required(
    'PartyListV2.view_restricted_guests',
    login_url='pub-permission_denied'
)
def restricted_lists(request):

    if request.method == "POST":
        if request.POST.get('blacklist') is not None:
            blacklist_form = RestrictedGuestForm(request.POST)
            if blacklist_form.is_valid():
                blacklisted_guest = blacklist_form.save(commit=False)
                blacklisted_guest.added_by = request.user
                blacklisted_guest.save()
                return HttpResponseRedirect(reverse(restricted_lists))
            graylist_form = RestrictedGuestForm()
        else:
            graylist_form = RestrictedGuestForm(request.POST)
            if graylist_form.is_valid():
                graylisted_guest = graylist_form.save(commit=False)
                graylisted_guest.graylisted = True
                graylisted_guest.added_by = request.user
                graylisted_guest.save()
                return HttpResponseRedirect(reverse(restricted_lists))
            blacklist_form = RestrictedGuestForm()

    else:
        blacklist_form = RestrictedGuestForm()
        graylist_form = RestrictedGuestForm()

    context = {
        'blacklist': [
            (
                guest,
                guest.can_be_deleted_by(request.user)
            )
            for guest in RestrictedGuest.objects.filter(graylisted=False).order_by('name')],
        'graylist': [
            (
                guest,
                guest.can_be_deleted_by(request.user)
            )
            for guest in RestrictedGuest.objects.filter(graylisted=True).order_by('name')],
        'blacklist_form': blacklist_form,
        'graylist_form': graylist_form
    }

    return render(request, 'partiesv2/restricted_lists.html', context)


@login_required
@permission_required("PartyListV2.view_parties")
@require_GET
def download_jobs(request, party_id):
    """
    View for downloading a resource
    """
    try:
        party = Party.objects.get(pk=party_id)
        path = party.jobs.path
        _, extension = os.path.splitext(path)
        name = party.name + " - Jobs" + extension
        return sendfile(
            request,
            path,
            attachment=True,
            attachment_filename=name
        )
    except (ValueError, Party.DoesNotExist):
        return redirect("partylist-index")

