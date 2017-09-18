"""
Views for PartyList app.
"""
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect

from .models import Party, BlacklistedGuest
from .forms import PartyForm, EditPartyInfoForm, BlacklistForm


@login_required
def index(request):
    """
    View for all parties
    """
    parties = Party.objects.all().order_by("date")
    context = {
        'all_parties': parties,
    }
    return render(request, 'parties/view.html', context)


@login_required
def guests(request, party_id):
    """
    View for all guests on the list for a party
    """
    try:
        requested_party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return redirect("partylist-index")
    party_mode = requested_party.is_party_mode()
    vouchers = frozenset(
        (user.username, user.get_full_name())
        for user in
        User.objects.filter(
            groups__name__in=['Brothers', 'Pledges']
        )
    )
    context = {
        'party': requested_party,
        'partymode': party_mode,
        'vouchers': vouchers,
    }
    return render(request, 'parties/guests.html', context)


@login_required
def view_blacklist(request):
    """
    View for viewing blacklist.
    """
    context = {
        'blacklist': BlacklistedGuest.objects.all()
    }
    return render(request, 'parties/blacklist/view.html', context)


@permission_required(
    'PartyList.manage_blacklist',
    login_url='pub-permission_denied',
)
def manage_blacklist(request):
    """
    View for managing blacklist.
    """
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
    return render(request, 'parties/blacklist/manage.html', context)


@permission_required(
    'PartyList.manage_blacklist',
    login_url='pub-permission_denied',
)
def remove_blacklisting(request, bl_id):
    """
    View for removing a blacklisted guest.
    """
    if request.method == 'POST':
        bl_guest = BlacklistedGuest.objects.get(pk=bl_id)
        bl_guest.delete()
    return redirect('partylist-manage_blacklist')


@permission_required(
    'PartyList.manage_parties',
    login_url='pub-permission_denied',
)
def add_party(request):
    """
    View for adding a party.
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
    return render(request, 'parties/add.html', context)


@permission_required(
    'PartyList.manage_parties',
    login_url='pub-permission_denied',
)
def manage_parties(request):
    """
    Provides a view to manage all of the parties in the system.
    """
    all_parties = Party.objects.all().order_by("date").reverse()
    context = {
        'all_parties': all_parties,
    }
    return render(request, 'parties/manage.html', context)


@permission_required(
    'PartyList.manage_parties',
    login_url='pub-permission_denied',
)
def edit_party(request, party_id):
    """
    Provides a view to edit a single party.
    """
    # Retrieve the party that we are trying to edit
    try:
        requested_party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return redirect("partylist-manage_parties")

    if request.method == 'POST':
        # If this is a POST request, the form has been submitted
        form = EditPartyInfoForm(request.POST, request.FILES,
                                 instance=requested_party)

        if form.is_valid():  # Check that form is valid
            form.save()
            return redirect("partylist-manage_parties")
    else:
        form = EditPartyInfoForm(instance=requested_party)

    context = {
        'requested_party': requested_party,
        'form': form,
        'error': form.errors
    }
    return render(request, 'parties/edit.html', context)


@permission_required(
    'PartyList.manage_parties',
    login_url='pub-permission_denied',
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
