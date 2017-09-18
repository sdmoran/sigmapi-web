"""
API for PartyList app.
"""
import csv
from datetime import datetime
import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Party, Guest, PartyGuest, BlacklistedGuest
from .forms import GuestForm


# TODO: Make this API follow REST standards
# For example, replace all those 500s with 4XXs


def user_can_edit(user=None, party_guest=None):
    """
    Return whether the given user can edit the party guest.

    Arguments:
        user (User)
        party_guest (PartyGuest)
    """
    return (
        user.has_perm('PartyList.can_destroy_any_party_guest') or
        party_guest.addedBy == user
    )


def get_full_guest(party_name, date, guest_id):
    """
    Get guest and party guest as a tuple.

    Arguments:
        party_name (str)
        date (datetime)
        guest_id (int)

    Returns: (Guest, PartyGuest)
    """
    guest = Guest.objects.get(id=guest_id)
    party = Party.objects.get(name__exact=party_name, date__exact=date)
    party_guest = PartyGuest.objects.get(party=party, guest=guest)
    return guest, party_guest


@login_required
@csrf_exempt
@permission_required('PartyList.add_partyguest')
def create(request, party_id):
    """
    Create a guest and party guest object for the given party.
    """
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)

    party = Party.objects.get(pk=party_id)

    # See if the guest already exists
    guest_name = request.POST.get('name')
    guest_gender = request.POST.get('gender')
    voucher_username = request.POST.get('vouchedForBy')
    guest = None

    added_by_result = _get_added_by(party, request.user, voucher_username)
    if isinstance(added_by_result, HttpResponse):
        return added_by_result
    added_by, was_vouched_for = added_by_result

    blacklist_response = _check_blacklisting(
        guest_name,
        guest_gender,
        request.POST.get('force'),
        added_by,
        was_vouched_for,
    )
    if blacklist_response:
        return blacklist_response

    try:
        guest = Guest.objects.get(
            name__exact=guest_name,
            gender__exact=guest_gender,
        )
    except Guest.DoesNotExist:
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save()
        else:
            return HttpResponse(
                'Error adding guest: invalid guest format. ' +
                'Contact webmaster.',
                status=500,
            )
    try:
        party_guest = PartyGuest.objects.get(
            party__exact=party,
            guest__exact=guest,
        )
    except PartyGuest.DoesNotExist:
        pass
    else:
        # if this guest is already on the list for this party
        if party_guest:
            return HttpResponse(
                'The guest you tried to add is already on the list.',
                status=409,
            )

    party_guest = PartyGuest(
        party=party,
        guest=guest,
        addedBy=added_by,
        wasVouchedFor=was_vouched_for,
    )
    party_guest.save()

    # Respond with the details on the party guest that was just added
    return HttpResponse(
        json.dumps(party_guest.to_json()),
        content_type="application/json",
    )


def _get_added_by(party, requesting_user, voucher_username):
    """
    Calculate who a guest should be listed as "addedBy".

    Arguments:
        party (Party)
        requesting_user (User): User that sent that HTTP request to add
        voucher_username (str|NoneType): Username of voucher. Is ignored
            if None or empty

    Returns: ((User, bool)|HttpResponse)
        - If not error, return pair of (
                user who is adding guest,
                whether they are a voucher
            )
        - If error, return HTTP response with error. Errors if we try
          to vouch while not in party mode or voucher username is invalid.
    """
    if not voucher_username:
        return requesting_user, False
    if not party.is_party_mode():
        return HttpResponse(
            'Cannot vouch while not in party mode.',
            status=409,
        )
    try:
        voucher = User.objects.get(username=voucher_username)
    except User.DoesNotExist:
        return HttpResponse(
            'Error vouching for guest: Invalid voucher username \'' +
            voucher_username + '\'.',
            status=422,
        )
    return voucher, True


def _check_blacklisting(
        guest_name,
        guest_gender,
        force,
        added_by,
        was_vouched_for
):
    """
    Return 4XX response iff blacklist rejects given guest.

    Arguments:
        guest_name (str)
        guest_gender (str)
        force (str): 'true' if we want to override blacklist match;
            otherwise, any other string on None
        added_by (str)
        was_vouched_for (bool)

    Returns: (HttpResponse|NoneType)
        HTTP response if blacklist match, else None.
    """
    if force == 'true':
        return None
    # Check to see if guest is on the blacklist before creating it
    for entry in BlacklistedGuest.objects.all():
        match = entry.check_match(guest_name)
        if not match:
            continue
        guest_dict = {
            'maybe_blacklisted': True,
            'blacklist_name': match.name,
            'blacklist_details': match.details,
            'attempted_name': guest_name,
            'attempted_gender': guest_gender,
        }
        if was_vouched_for:
            guest_dict['attempted_voucher'] = added_by.username
        # Respond with the details on the party guest that was just added
        return HttpResponse(
            json.dumps(guest_dict),
            content_type='application/json'
        )
    return None


@login_required
@csrf_exempt
def update_manual_delta(request, party_id):
    """
    Manually update deltas.

    Called when the + or - buttons are pressed.
    """
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    party = Party.objects.get(pk=party_id)
    try:
        gender = request.POST.get('gender')
        delta = int(request.POST.get('delta'))
    except (KeyError, ValueError):
        return HttpResponse(
            'Error: Invalid gender or count parameters.' +
            ' Contact webmaster.',
            status=500,
        )

    if gender == 'M':
        party.guy_delta += delta
    elif gender == 'F':
        party.girl_delta += delta
    else:
        return HttpResponse(
            'Error: Invalid gender parameter.' +
            ' Contact webmaster.',
            status=500
        )

    party.save()

    response = {}
    response['guycount'] = party.guycount + party.guy_delta
    response['girlcount'] = party.girlcount + party.girl_delta

    return HttpResponse(
        json.dumps(response),
        content_type='application/json',
    )


@login_required
def poll_count(_request, party_id):
    """
    Poll the guest count
    """
    try:
        party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return HttpResponse("Error: Party not found.", status=500)

    response = {
        'guycount': party.guycount + party.guy_delta,
        'girlcount': party.girlcount + party.girl_delta,
        'guys_ever_signed_in': party.guys_ever_signed_in,
        'girls_ever_signed_in': party.girls_ever_signed_in,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
@csrf_exempt
def sign_in(
        request,
        party_id,  # pylint: disable=unused-argument
        party_guest_id
):  # pylint: disable=unused-argument
    """
    Sign-in a guest with given ID.
    """
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        party_guest = PartyGuest.objects.get(pk=party_guest_id)
    except (Party.DoesNotExist, PartyGuest.DoesNotExist):
        return HttpResponse(
            'Error signing in guest.' +
            ' Contact webmaster.',
            status=500,
        )
    if not party_guest.signedIn:
        party_guest.signedIn = True
        _modify_count(party, party_guest.guest.gender, 1)
        if party_guest.everSignedIn is False:
            party_guest.everSignedIn = True
            party_guest.timeFirstSignedIn = datetime.now()
            if party_guest.guest.gender == 'M':
                party.guys_ever_signed_in += 1
            elif party_guest.guest.gender == 'F':
                party.girls_ever_signed_in += 1
            party.save()
        party_guest.save()
        return HttpResponse('Guest signed in.', status=200)
    else:
        return HttpResponse(
            'Guest already signed in. Refresh to see updated list.',
            status=409
        )


@login_required
@csrf_exempt
def sign_out(
        request,
        party_id,  # pylint: disable=unused-argument
        party_guest_id,
):
    """
    Sign out a guest with given id
    """
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        party_guest = PartyGuest.objects.get(pk=party_guest_id)
    except (Party.DoesNotExist, PartyGuest.DoesNotExist):
        return HttpResponse(
            'Error signing out guest.' +
            ' Contact webmaster.',
            status=500,
        )
    if party_guest.signedIn:
        party_guest.signedIn = False
        _modify_count(party, party_guest.guest.gender, -1)
        party_guest.save()
        return HttpResponse('Guest signed out.', status=200)
    return HttpResponse(
        'Guest already signed out. Refresh to see updated list.',
        status=409,
    )


@login_required
@csrf_exempt
def destroy(
        request,
        party_id,  # pylint: disable=unused-argument
        party_guest_id,
):
    """
        Delete a guest (keyd by the supplied id),
        so long as the current user has domain over them
    """
    if request.method != 'DELETE':
        return HttpResponse(
            'Endpoint supports DELETE method only.',
            status=405
        )
    try:
        party = Party.objects.get(pk=party_id)
        party_guest = PartyGuest.objects.get(pk=party_guest_id)
    except (Party.DoesNotExist, PartyGuest.DoesNotExist):
        return HttpResponse(
            'Error deleting guest: guest or party does not exist.',
            status=409,
        )
    if user_can_edit(user=request.user, party_guest=party_guest):
        if party_guest.signedIn:
            _modify_count(party, party_guest.guest.gender, -1)
        party_guest.delete()
        return HttpResponse('Guest deleted', status=200)
    return HttpResponse(
        'Error deleting guest: permission denied.',
        status=401
    )


@login_required
def export_list(_request, party_id):
    """
    Export the guest list as a csv file.

    This uses the native csv module that comes bundled with python.
    Using excel would require a 3rd party module, and hardly provides benefits
    over a standard csv format.
    """
    requested_party = Party.objects.get(pk=party_id)
    party_guests = PartyGuest.objects.filter(
        party__exact=requested_party
    ).order_by('guest__name')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guests.csv"'
    writer = csv.writer(response)

    writer.writerow(['Female Guests'])
    writer.writerow(['Name', 'Signed In'])
    female_guests = party_guests.filter(guest__gender__exact='F')
    for party_guest in female_guests:
        writer.writerow([party_guest.guest.name, str(party_guest.signedIn)])

    writer.writerow(['Male Guests'])
    writer.writerow(['Name', 'Signed In'])
    male_guests = party_guests.filter(guest__gender__exact='M')
    for party_guest in male_guests:
        writer.writerow([party_guest.guest.name, str(party_guest.signedIn)])

    return response


@login_required
def poll(request, party_id):
    """
    Called by the client to check for guests added after a given time.

    This allows each clients guest list to be updated in partial real time.
    Checks the guests object for new guests added after a supplied time
    (unix format) and sends a JSON object of those guests back.
    """
    last_stamp = float(request.GET.get('last'))
    # JS timestamp is in milliseconds, time_t is in seconds.
    last = datetime.fromtimestamp(last_stamp / 1000.0)
    gender = request.GET.get('gender')
    guests = PartyGuest.objects.filter(
        createdAt__gte=last,
        guest__gender__exact=gender,
        party__id__exact=party_id,
    )
    response = {}
    response['guests'] = [guest.to_json() for guest in guests]
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def init_pulse(request, party_id):
    """
    Return to the caller the current user ID and whether it's in party mode.
    """
    requested_party = Party.objects.get(pk=party_id)
    response = {}
    response['partymode'] = requested_party.is_party_mode()
    response['userID'] = request.user.id
    response['canDestroyAnyGuest'] = request.user.has_perm(
        'PartyList.can_destroy_any_party_guest'
    )
    return HttpResponse(json.dumps(response), content_type="application/json")


def _modify_count(party, gender, delta):
    """
    Modify the guycount or girlcount of a party.

    Arguments:
        party (Party)
        gender (str): 'M' or 'F'
        delta (int)
    """
    if gender == 'M':
        party.guycount += delta
    elif gender == 'F':
        party.girlcount += delta
    party.save()
