import csv

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpRequest

from apps.PartyListV2.models import Party, PartyGuest, RestrictedGuest
import json


def json_response(response):
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def modify_party_count(request, party_id):
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        if not party.is_list_closed():
            return HttpResponse('Cannot modify list count until the party starts', status=403)

        gender = request.POST.get('gender')
        sign = request.POST.get('sign')

        if gender == "M":
            if sign == "1":
                party.guycount += 1
            elif sign == "-1":
                party.guycount -= 1
            else:
                HttpResponse('Invalid sign (must be 1 or -1)', status=400)
        elif gender == "F":
            if sign == "1":
                party.girlcount += 1
            elif sign == "-1":
                party.girlcount -= 1
            else:
                HttpResponse('Invalid sign (must be 1 or -1)', status=400)
        else:
            return HttpResponse('Invalid gender supplied', status=400)

        party.save()

        return json_response({
            "party": party.to_json()
        })
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)


@login_required
def party_pulse(request, party_id):
    if request.method != 'GET':
        return HttpResponse('Endpoint supports GET method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        return json_response({
            "lastUpdated": party.last_updated.timestamp(),
            "guestUpdateCounter": party.guest_update_counter,
            "listClosed": party.is_list_closed()
        })
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)



@permission_required('PartyListV2.door_access', raise_exception=True)
def sign_out(request, party_id, party_guest_id):
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        party_guest = PartyGuest.objects.get(pk=party_guest_id)
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)
    except PartyGuest.DoesNotExist:
        return HttpResponse('Requested Party Guest does not exist.', status=404)

    if not party.is_list_closed():
        return HttpResponse("Can't sign out guests before the party starts.", status=403)

    if party_guest.signed_in:
        party.sign_out(party_guest)

        party.save()
        party_guest.save()
        return json_response(party_guest.to_json())
    else:
        return HttpResponse(
            'Guest already signed out. Refresh to see updated list.',
            status=409
        )


@permission_required('PartyListV2.door_access', raise_exception=True)
def sign_in(request, party_id, party_guest_id):
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)
    try:
        party = Party.objects.get(pk=party_id)
        party_guest = PartyGuest.objects.get(pk=party_guest_id)
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)
    except PartyGuest.DoesNotExist:
        return HttpResponse('Requested Party Guest does not exist.', status=404)

    if not party.is_list_closed():
        return HttpResponse("Can't sign in guests before the party starts.", status=403)

    if not party_guest.signed_in:
        party.sign_in(party_guest)

        party.save()
        party_guest.save()
        return json_response(party_guest.to_json())
    else:
        return HttpResponse(
            'Guest already signed in. Refresh to see updated list.',
            status=409
        )

@login_required
def destroy_guest(request, party_id, party_guest_id):

    if request.method != 'DELETE':
        return HttpResponse('Endpoint supports DELETE method only.', status=405)

    try:
        party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)

    if party.is_list_closed():
        return HttpResponse("You cannot delete a guest after the party list closes.", status=403)

    try:
        guest = PartyGuest.objects.get(pk=party_guest_id)
    except PartyGuest.DoesNotExist:
        return HttpResponse("The guest you are trying to delete does not exist.", status=404)

    if (guest.added_by == request.user or
            request.user.has_perm("PartyListV2.can_destroy_any_party_guest")):
        guest.delete()

        party.guest_update_counter += 1
        party.update_timestamp()
        party.save()

        return HttpResponse("The guest has been deleted.", status=200)
    else:
        return HttpResponse("You do not have permission to delete this guest", status=401)



@permission_required("PartyListV2.view_parties")
def get_details(request, party_id):
    try:
        requested_party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)

    return json_response({
        "party": requested_party.to_json()
    })


@permission_required("PartyListV2.view_parties")
def get_guests(request, party_id):
    guests = PartyGuest.objects.filter(party__id=party_id).order_by(Lower("name")).only("_cached_json")
    response = {
        "guests": [guest.cached_json for guest in guests]
    }
    return json_response(response)


@permission_required("PartyListV2.view_parties")
def get_delta_guests(request, party_id, update_counter):
    guests = PartyGuest.objects.filter(party__id=party_id, update_counter__gt=update_counter)
    guest_ids = PartyGuest.objects.filter(party__id=party_id).values_list('id', flat=True).all()
    response = {
        "guests": [guest.cached_json for guest in guests],
        "guestIds": [id for id in guest_ids]
    }
    return json_response(response)


@permission_required("PartyListV2.view_parties")
def get_restricted_guests(request, party_id):
    response = {
        "restrictedGuests": [guest.to_json() for guest in RestrictedGuest.objects.all()]
    }
    return json_response(response)


@login_required
def get_permissions(request, party_id):
    # These are enforced server side as well
    response = {
        "permissions": {
            "canRemoveAnyGuest": request.user.has_perm("PartyListV2.can_destroy_any_party_guest"),
            "canAddPartyGuests": request.user.has_perm("PartyListV2.add_party_guests"),
            "youHaveDoorAccess": request.user.has_perm("PartyListV2.door_access"),
        }
    }
    return json_response(response)

@permission_required(
    "PartyListV2.add_party_guests"
)
def create_guest(request, party_id):
    """
    Create a guest and party guest object for the given party.
    """
    if request.method != 'POST':
        return HttpResponse('Endpoint supports POST method only.', status=405)

    # Retreive the party instance
    try:
        party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        return HttpResponse('Requested Party ID does not exist.', status=404)

    # Retrieve the new guest's name
    guest_name = request.POST.get('name')
    if guest_name is None or guest_name.strip() is "":
        return HttpResponse("Must supply guest name.", status=400)

    # Retrieve the new guest's gender
    guest_gender = request.POST.get('gender')
    if guest_gender is None or not (guest_gender is "M" or guest_gender is "F"):
        return HttpResponse('Guest gender must be "M" or "F".', status=400)

    # Check if the guest is already on the list
    exists = PartyGuest.objects.filter(name__iexact=guest_name,
                                       party=party,
                                       gender=guest_gender).count() > 0
    if exists:
        return HttpResponse("Guest with that name already exists.", status=409)

    # Retrieve the brother selected from the dropdown box (either borrowed invite or vouching)
    selected_brother_username = request.POST.get('selectedBrother')
    if selected_brother_username is not None and not selected_brother_username.strip() == "":
        try:
            selected_brother = User.objects.get(username=selected_brother_username)
        except User.DoesNotExist:
            selected_brother = None
    else:
        selected_brother = None

    # If we are still in regular list mode
    if not party.is_list_closed():
        preparty_access = request.POST.get("prepartyAccess") == "true"

        limit_check = __check_invite_limit(preparty_access, party, selected_brother, request)
        if limit_check:
            return limit_check  # User reached some type of invite limit, return the message

        if selected_brother is not None and selected_brother.id == request.user.id:
            return HttpResponse("You cannot borrow an invite from yourself (nice try).", status=403)

        invite_used = selected_brother
        was_vouched_for = False
        added_by = request.user

    else:  # Party is active
        if selected_brother is None:
            return HttpResponse("You must list a vouching brother when the list is in party mode.", status=400)

        # Force Add indicates we have already gone through the confirmation modal on client side
        risk_approval = request.POST.get("riskApproval") == "true"

        if party.user_reached_vouching_limit(selected_brother) and not risk_approval:
            return HttpResponse("The vouching brother has reached their vouch limit, you will need the risk manager"
                                " or president to authorize this addition.", status=403)

        if not request.user.has_perm("PartyListV2.door_access"):
            return HttpResponse("You do not have permission to create guests after the list has closed.", status=403)

        added_by = selected_brother
        invite_used = None
        preparty_access = party.is_preparty_mode()
        was_vouched_for = True

    party_guest = PartyGuest(
        name=guest_name[:90],
        gender=guest_gender,
        party=party,
        added_by=added_by,
        was_vouched_for=was_vouched_for,
        invite_used=invite_used,
        has_preparty_access=preparty_access
    )
    party_guest.save()

    party.update_timestamp()
    party.save()

    return json_response(party_guest.to_json())


def __check_invite_limit(preparty_access: bool, party: Party, selected_brother: User, request: HttpRequest):
    if preparty_access:
        # Check to make sure the user hasn't reached their limit (and the person they are
        # borrowing invites from hasn't either)
        if party.has_preparty_invite_limits:
            if selected_brother is None and party.user_reached_preparty_limit(request.user):
                return HttpResponse("You have reached your pre-party invite limit.", status=403)
            elif selected_brother is not None and party.user_reached_preparty_limit(selected_brother):
                return HttpResponse("The brother you are trying to borrow invites from has "
                                    "reached their pre-party invite limit.", status=403)
        elif party.has_party_invite_limits:
            if selected_brother is None and party.user_reached_party_limit(request.user):
                return HttpResponse("You have pre-party invites left, but your total "
                                    "amount of guests has reached the limit for this party. Try "
                                    "removing a regular guest before adding another to pre-party.", status=403)
            elif selected_brother is not None:
                if party.user_reached_party_limit(selected_brother):
                    return HttpResponse("The brother you are trying to borrow invites"
                                        " from has reached their party invite limit.", status=403)
                elif party.user_reached_preparty_limit(selected_brother):
                    return HttpResponse("The brother you are trying to borrow invites"
                                        " from has reached their pre-party invite limit.", status=403)
    else:
        if party.has_party_invite_limits:
            if selected_brother is None and party.user_reached_party_limit(request.user):
                return HttpResponse("You have reached your party invite limit.", status=403)
            elif selected_brother is not None and party.user_reached_party_limit(selected_brother):
                return HttpResponse("The brother you are trying to borrow invites "
                                    "from has reached their party invite limit.", status=403)

    return False


@permission_required("PartyListV2.view_parties")
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
    ).order_by('name')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guests.csv"'
    writer = csv.writer(response)

    writer.writerow(['Female Guests'])
    writer.writerow(['Name', 'Signed In', 'Time First Signed In'])
    female_guests = party_guests.filter(gender__exact='F')
    for party_guest in female_guests:
        writer.writerow([party_guest.name, str(party_guest.signed_in), str(party_guest.formatted_time_first_signed_in())])

    writer.writerow(['Male Guests'])
    writer.writerow(['Name', 'Signed In', 'Time First Signed In'])
    male_guests = party_guests.filter(gender__exact='M')
    for party_guest in male_guests:
        writer.writerow([party_guest.name, str(party_guest.signed_in), str(party_guest.formatted_time_first_signed_in())])

    return response


@permission_required('PartyListV2.manage_parties')
def refresh_guest_json(request):
    guests = PartyGuest.objects.all()
    for guest in guests:
        guest.save()
    return HttpResponse("Guest JSON Refreshed.", status=200)
