from django.contrib.auth.decorators import login_required
from .models import Party, Guest, PartyGuest, BlacklistedGuest
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .widgets import GuestForm

import json
import csv


"""
    ATTENTION: If we're going to make an API, let's do our
        best to keep it RESTful accordin got w3 standards:
        http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
"""

def userCanEdit(user=None,pg=None):
    """return true if the given user can edit the party guest making this function
    allows us to add more cases in which a type of user can edit a guest"""
    if user.has_perm('PartyList.can_destroy_any_party_guest'):
        return True

    if pg.addedBy == user:
        return True

    return False

def getFullGuest(party, date, id):
    """get a guest and its associated partyGuest model, return as a tuple"""
    guest = Guest.objects.get(id=id)
    party = Party.objects.get(name__exact=party, date__exact=date)
    pGuest = PartyGuest.objects.get(party=party,guest=guest)

    return guest,pGuest

@login_required
@csrf_exempt
@permission_required('PartyList.add_partyguest')
def create(request, party):
    """
        create a guest object as well as a partyguest object for the given party
    """
    if request.method == 'POST':
        partyObj = Party.objects.get(pk=party)

        # See if the guest already exists
        guestName = request.POST.get('name')
        guestGender = request.POST.get('gender')
        guest = None

        if request.POST.get("force") != "true":
            # Check to see if guest is on the blacklist before creating it
            for entry in BlacklistedGuest.objects.all():
                match = entry.check_match(guestName)
                if not match:
                    continue
                guest_dict = {
                    'maybe_blacklisted': True,
                    'blacklist_name': match.name,
                    'blacklist_details': match.details,
                    'attempted_name': guestName,
                    'attempted_gender': guestGender,
                }
                # Respond with the details on the party guest that was just added
                return HttpResponse(
                    json.dumps(guest_dict),
                    content_type='application/json'
                )
        try:
            guest = Guest.objects.get(name__exact=guestName,
                                      gender__exact=guestGender)
        except:
            pass # Don't need to do anything if failed to find the guest

        if guest: # If the guest already exists, check if it exists for the party already
            try:
                partyguest = PartyGuest.objects.get(party__exact=partyObj, guest__exact=guest)

                if partyguest: # if this guest is already on the list for this party
                    return HttpResponse('The guest you tried to add is already on the list.', status=409)
            except:
                pass
        else:
            # Otherwise, if the guest does not exist we create it for later
            form = GuestForm(request.POST)
            if form.is_valid():
                guest = form.save()
            else:
                return HttpResponse('Error adding guest: invalid guest format. Contact webmaster.', status=500)

        pGuest = PartyGuest(party=partyObj, guest=guest, addedBy=request.user)
        pGuest.save()

        # Respond with the details on the party guest that was just added
        return HttpResponse(json.dumps(pGuest.toJSON()), content_type="application/json")
    else:
        return HttpResponse('Endpoint supports POST method only.', status=405)

@login_required
@csrf_exempt
def updateCount(request, party):
    """
        Adjust the guest count for a given party and gender
    """

    if request.method == 'POST':
        partyObj = Party.objects.get(pk=party)
        try:
            gender = request.POST.get('gender')
            delta = int(request.POST.get('delta'))
        except:
            return HttpResponse('Error: Invalid gender or count parameters. Contact webmaster.', status=500)

        if gender == 'M':
            partyObj.guycount = PartyGuest.objects.filter(party_id=party, signedIn=True, guest__gender='M').count() + \
                partyObj.guy_delta
        elif gender == 'F':
            partyObj.girlcount = PartyGuest.objects.filter(party_id=party, signedIn=True, guest__gender='F').count() + \
                partyObj.girl_delta
        else:
            return HttpResponse('Error: Invalid gender parameter. Contact webmaster.', status=500)


        partyObj.save()

        response = {}
        response['guycount'] = partyObj.guycount
        response['girlcount'] = partyObj.girlcount

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse('Endpoint supports POST method only.', status=405)

@login_required
@csrf_exempt
def updateManualDelta(request, party):
    """
    Called when the + or - buttons are pressed.  Manually updates deltas.
    """
    if request.method == 'POST':
        partyObj = Party.objects.get(pk=party)
        try:
            gender = request.POST.get('gender')
            delta = int(request.POST.get('delta'))
        except:
            return HttpResponse('Error: Invalid gender or count parameters. Contact webmaster.', status=500)

        if gender == 'M':
            partyObj.guy_delta += delta
            partyObj.guycount += delta
        elif gender == 'F':
            partyObj.girl_delta += delta
            partyObj.girlcount += delta
        else:
            return HttpResponse('Error: Invalid gender parameter. Contact webmaster.', status=500)

        partyObj.save()

        response = {}
        response['guycount'] = partyObj.guycount
        response['girlcount'] = partyObj.girlcount

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse('Endpoint supports POST method only.', status=405)

@login_required
def pollCount(request, party):
    """
        Poll the guest count
    """
    try:
        partyObj = Party.objects.get(pk=party)
    except:
        return HttpResponse("Error: Party not found.", status=500)

    response = {}
    response['guycount'] = partyObj.guycount
    response['girlcount'] = partyObj.girlcount

    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
@csrf_exempt
def signin(request, party, guestID):
    """
        Signin a guest with given ID
    """
    if request.method == 'POST':
        try:
            partyGuest = PartyGuest.objects.get(pk=guestID)
            partyGuest.signedIn = True

            if partyGuest.everSignedIn == False:
                partyGuest.everSignedIn = True
                partyGuest.timeFirstSignedIn = datetime.now()

            partyGuest.save()
        except:
            return HttpResponse('Error signing in guest. Contact webmaster.', status=500)

        return HttpResponse('Guest signed in.', status=200)
    else:
        return HttpResponse('Endpoint supports POST method only.', status=405)

@login_required
@csrf_exempt
def signout(request, party, guestID):
    """
        Sign out a guest with given id
    """
    if request.method == 'POST':
        try:
            partyGuest = PartyGuest.objects.get(pk=guestID)
            partyGuest.signedIn = False
            partyGuest.save()
        except:
            return HttpResponse('Error signing out guest. Contact webmaster.', status=500)

        return HttpResponse('Guest signed out.', status=200)
    else:
        return HttpResponse('Endpoint supports POST method only.', status=405)

@login_required
@csrf_exempt
def destroy(request, party, guestID):
    """
        Delete a guest (keyd by the supplied id), so long as the current user has domain over them
    """
    if request.method == 'DELETE':
        try:
            partyGuest = PartyGuest.objects.get(pk=guestID)
        except:
            return HttpResponse('Error deleting guest: guest does not exist.', status=409)

        if userCanEdit(user=request.user, pg=partyGuest):
            partyGuest.delete()

            return HttpResponse("Guest deleted", status=200)
        else:
            return HttpResponse('Error deleting guest: permission denied.', status=401)
    else:
        return HttpResponse('Endpoint supports DELETE method only.', status=405)


@login_required
def export_list(request, party):
    """
    export the guest list as a csv file. This uses the native csv module
    that comes bundled with python. Using excel would require a 3rd party
    module, and hardly provides benefits over a standard csv format
    """

    requested_party = Party.objects.get(pk=party)

    partyguests = PartyGuest.objects.filter(party__exact=requested_party).order_by('guest__name')

    femaleGuests = partyguests.filter(guest__gender__exact="F")
    maleGuests = partyguests.filter(guest__gender__exact="M")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guests.csv"'

    writer = csv.writer(response)

    writer.writerow(['Female Guests'])
    writer.writerow(['Name', 'Signed In'])

    for pg in femaleGuests:
        writer.writerow([pg.guest.name, str(pg.signedIn)])

    writer.writerow(['Male Guests'])
    writer.writerow(['Name', 'Signed In'])

    for pg in maleGuests:
        writer.writerow([pg.guest.name, str(pg.signedIn)])

    return response

@login_required
def poll(request, party):
    """
    called by the client to check for guests added after a given time.
    This allows each clients guest list to be updated in partial real time

        Checks the guests object for new guests added
        after a supplied time (unix format) and sends
        a json object of those guests back
    """
    last_stamp = float(request.GET.get('last'))
    last = datetime.fromtimestamp(last_stamp/1000.0) # js timestamp is in milliseconds, time_t is in seconds.

    gender = request.GET.get('gender')

    guests = PartyGuest.objects.filter(createdAt__gte=last, guest__gender__exact=gender, party__id__exact=party)

    response = {}
    response['guests'] = [guest.toJSON() for guest in guests]

    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def initPulse(request, party):
    """
        Returns to the caller the current user ID and whether or not it is party mode
    """

    requested_party = Party.objects.get(pk=party)

    response = {}
    response['partymode'] = requested_party.isPartyMode()
    response['userID'] = request.user.id
    response['canDestroyAnyGuest'] = request.user.has_perm('PartyList.can_destroy_any_party_guest')

    return HttpResponse(json.dumps(response), content_type="application/json")
