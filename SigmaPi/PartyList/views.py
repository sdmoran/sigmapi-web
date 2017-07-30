from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from PartyList.models import Party
from django.http import HttpResponse
from PartyList.widgets import PartyForm, EditPartyInfoForm, BlacklistForm
from PartyList.models import BlacklistedGuest
import json

@login_required
def index(request):
    """
        View for all parties
    """

    parties = Party.objects.all().order_by("date")
    context = {
        'all_parties': parties,
    }
    return render(request, 'parties.html', context)

@login_required
def guests(request, party):
    """
        View for all guests on the list for a party
    """

    try:
        requested_party = Party.objects.get(pk=party)
    except:
        return redirect("PartyList.views.index")

    partymode = requested_party.isPartyMode()

    context = {
            'party': requested_party,
            'partymode': partymode,
    }

    return render(request, 'partyguests.html', context)


@login_required
def view_blacklist(request):

    context = {
        'blacklist': BlacklistedGuest.objects.all()
    }

    return render(request, 'blacklist.html', context)

@permission_required('PartyList.manage_blacklist', login_url='PubSite.views.permission_denied')
def manage_blacklist(request):
    context = {
        'blacklist': BlacklistedGuest.objects.all(),
        'message': None
    }

    if request.method == 'POST':
        form = BlacklistForm(request.POST)
        if form.is_valid():
            # Set details to empty string if blank
            new_blacklisted_guest = form.save(commit=False)
            if not form.cleaned_data['details']:
                new_blacklisted_guest.details = ''
            new_blacklisted_guest.save()
            context['message'] = 'Successfully added entry to blacklist'
        else:
            context['message'] = 'Error adding entry to blacklist'
    else:
        form = BlacklistForm()

    context['form'] = form

    return render(request, 'manage_blacklist.html', context)


@permission_required('PartyList.manage_blacklist', login_url='PubSite.views.permission_denied')
def remove_blacklisting(request, bl_id):

    if request.method == 'POST':
        bl_guest = BlacklistedGuest.objects.get(pk=bl_id)

        bl_guest.delete()

        context = {
            'blacklist': BlacklistedGuest.objects.all()
        }

        return redirect('PartyList.views.manage_blacklist')

    return redirect('PartyList.views.manage_blacklist')


@permission_required('PartyList.manage_parties', login_url='PubSite.views.permission_denied')
def add_party(request):
    """
        Provides a view to add a party.
    """
    context = {
        'message': []
    }

    if request.method == 'POST':
        form = PartyForm(request.POST)
        if form.is_valid():
            party = form.save()
            context['message'].append(party.name + " successfully added.")
        else:
            context['message'].append("Error adding party.")

    return render(request, 'add_party.html', context)

@permission_required('PartyList.manage_parties', login_url='PubSite.views.permission_denied')
def manage_parties(request):
    """
        Provides a view to manage all of the parties in the system.
    """

    all_parties = Party.objects.all().order_by("date").reverse()

    context = {
        'all_parties': all_parties,
    }

    return render(request, 'manage_parties.html', context)

@permission_required('PartyList.manage_parties', login_url='PubSite.views.permission_denied')
def edit_party(request, party):
    """
        Provides a view to edit a single party.
    """
    # Retrieve the party that we are trying to edit
    try:
        requested_party = Party.objects.get(pk=party)
    except:
        return redirect("PartyList.views.manage_parties")

    errors = None

    if request.method == 'POST':
        # If this is a POST request, the form has been submitted
        form = EditPartyInfoForm(request.POST, request.FILES, instance=requested_party)

        if form.is_valid(): # Check that form is valid
            form.save()
            return redirect("PartyList.views.manage_parties")
    else:
        form = EditPartyInfoForm(instance=requested_party)

    context = {
        'requested_party': requested_party,
        'form': form,
        'error': form.errors
    }

    return render(request, 'edit_party.html', context)

@permission_required('PartyList.manage_parties', login_url='PubSite.views.permission_denied')
def delete_party(request, party):
    """
        Deletes the party with the ID that is sent in the post request
    """

    if request.method == 'POST':
        try:
            party = Party.objects.get(pk=party)
        except:
            return redirect("PartyList.views.manage_parties")

        party.delete()

    return redirect("PartyList.views.manage_parties")
