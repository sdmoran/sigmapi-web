from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Standards import notify
from Standards.forms import SummonsRequestForm, ArchiveSummonsForm
from Standards.models import SummonsRequest, Summons, SummonsHistoryRecord


@login_required
def index(request):
    """
        Displays the homepage of the standards module.
    """
    summons_form = SummonsRequestForm()
    summons_history = SummonsHistoryRecord.objects.all().filter(summonee=request.user).order_by('-date')

    error = None
    msg = None

    try:
        error = request.session['standards_index_error']
        del request.session['standards_index_error']
    except KeyError:
        pass

    try:
        msg = request.session['standards_index_msg']
        del request.session['standards_index_msg']
    except KeyError:
        pass

    context = {
        'error': error,
        'summons_form': summons_form,
        'msg': msg,
        'summons_history': summons_history
    }

    return render(request, "secure/standards_index.html", context)


@permission_required('Standards.add_summonsrequest', login_url='pub-permission_denied')
def send_summons_request(request):
    """
        A view for sending a summons request.
    """

    if request.method == 'POST':

        numRecipients = int(request.POST["recipient-count"])

        # Check for reason
        spokeWithStr = request.POST.get("spokeWith", "error")
        spokeWith = False
        if spokeWithStr == "yes":
            spokeWith = True
        elif spokeWithStr != "no":
            request.session['standards_index_error'] = "Summons request failed to send. You must fill in all fields."
            return redirect(index)
        outcomes = request.POST.get("outcomes", "")
        standards_action = request.POST.get("standards_action", "")
        special_circumstance = request.POST.get("special_circumstance", "")

        if spokeWith:
            if len(outcomes.strip()) == 0:
                request.session[
                    'standards_index_error'] = "Summons request failed to send. You must include outcomes of the conversation."
                return redirect(index)
            elif len(standards_action.strip()) == 0:
                request.session[
                    'standards_index_error'] = "Summons request failed to send. You must include suggested further action by standards."
                return redirect(index)
        elif len(special_circumstance.strip()) == 0:
            request.session[
                'standards_index_error'] = "Summons request failed to send. You must include the special circumstance."
            return redirect(index)

        # Check for recipients
        summonsSent = 0
        for i in range(numRecipients):
            try:
                if i == 0:
                    currentRecipient = request.POST["summonee"]
                else:
                    currentRecipient = request.POST["summonee_" + str(i + 1)]

                if len(currentRecipient.strip()) > 0:
                    recipientInt = int(currentRecipient)

                    recipientUser = User.objects.get(pk=recipientInt)

                    summonsReq = SummonsRequest(summoner=request.user, summonee=recipientUser, spokeWith=spokeWith,
                                                outcomes=outcomes, standards_action=standards_action,
                                                special_circumstance=special_circumstance,
                                                dateRequestSent=datetime.now())
                    summonsReq.save()

                    summonsSent += 1
            except:
                request.session[
                    'standards_index_error'] = "Unknown error occurred while processing summons recipient list. Please try again. If the problem persists, please contact the Web Chair."
                return redirect(index)

        if summonsSent > 0:
            request.session['standards_index_msg'] = "Summons request sent successfully!"

            notify.summons_requested(summonsSent)

            return redirect(index)
        else:
            request.session[
                'standards_index_error'] = "Summons request failed to send. You must include atleast 1 recipient with the request."
            return redirect(index)

    return redirect(index)


@permission_required('Standards.change_summonsrequest', login_url='pub-permission_denied')
def manage_summons_requests(request):
    """
        A view for managing summons requests and sending out summons.
    """

    current_requests = SummonsRequest.objects.all().order_by('-dateRequestSent')

    error = None
    msg = None

    try:
        error = request.session['standards_summons_error']
        del request.session['standards_summons_error']
    except KeyError:
        pass

    try:
        msg = request.session['standards_summons_msg']
        del request.session['standards_summons_msg']
    except KeyError:
        pass

    context = {
        'current_requests': current_requests,
        'error': error,
        'msg': msg
    }

    return render(request, "secure/standards_summons_requests.html", context)


@permission_required('Standards.delete_summonsrequest', login_url='pub-permission_denied')
def reject_summons_request(request, summons_req):
    """
        A view for denying a summons request.
    """

    if request.method == 'POST':
        try:
            summons_request = SummonsRequest.objects.get(pk=summons_req)
        except:
            request.session[
                'standards_summons_error'] = "Sorry, that summons request no longer exists. It may have been approved or rejected already."
            return redirect(manage_summons_requests)

        notify.summons_request_denied(summons_request)

        summons_request.delete()
        request.session['standards_summons_msg'] = "Summons request successfully rejected."
        return redirect(manage_summons_requests)
    else:
        return redirect(manage_summons_requests)


@permission_required('Standards.change_summonsrequest', login_url='pub-permission_denied')
def approve_summons_request(request, summons_req):
    """
        A view for approving a summons request.
    """
    if request.method == 'POST':
        try:
            summons_request = SummonsRequest.objects.get(pk=summons_req)
        except:
            request.session[
                'standards_summons_error'] = "Sorry, that summons request no longer exists. It may have been approved or rejected already."
            return redirect(manage_summons_requests)

        approved_summons = Summons()
        approved_summons.summoner = summons_request.summoner
        approved_summons.summonee = summons_request.summonee
        approved_summons.approver = request.user
        approved_summons.spokeWith = summons_request.spokeWith
        approved_summons.outcomes = summons_request.outcomes
        approved_summons.standards_action = summons_request.standards_action
        approved_summons.special_circumstance = summons_request.special_circumstance
        approved_summons.dateSummonsSent = datetime.now()

        approved_summons.save()
        summons_request.delete()

        notify.summons_sent(approved_summons)

        request.session['standards_summons_msg'] = "Summons request successfully accepted."
        return redirect(manage_summons_requests)
    else:
        return redirect(manage_summons_requests)


@permission_required('Standards.change_summons', login_url='pub-permission_denied')
def manage_summons(request):
    """
        View for editing/managing all summons
    """

    all_summons = Summons.objects.order_by('-dateSummonsSent')
    archive_summons = ArchiveSummonsForm()

    summons_history = SummonsHistoryRecord.objects.all().order_by('-date')

    error = None
    msg = None

    try:
        error = request.session['standards_summons_error']
        del request.session['standards_summons_error']
    except KeyError:
        pass

    try:
        msg = request.session['standards_summons_msg']
        del request.session['standards_summons_msg']
    except KeyError:
        pass

    context = {
        'all_summons': all_summons,
        'error': error,
        'msg': msg,
        'summons_history': summons_history,
        'archive_summons_form': archive_summons
    }

    return render(request, "secure/standards_summons.html", context)


@permission_required('Standards.change_summons', login_url='pub-permission_denied')
def accept_summons(request, summons):
    """
        Accept a summons and turn it into a SummonsHistoryRecord object.
    """

    if request.method == 'POST':
        try:
            summons_obj = Summons.objects.get(pk=summons)
        except:
            request.session[
                'standards_summons_error'] = "Sorry, that summons no longer exists. It may have been approved or rejected already."
            return redirect(manage_summons)

        form = ArchiveSummonsForm(request.POST)

        if form.is_valid():

            summonsHistory = SummonsHistoryRecord()
            summonsHistory.summonee = summons_obj.summonee
            summonsHistory.summoner = summons_obj.summoner
            summonsHistory.saved_by = request.user
            summonsHistory.details = form.cleaned_data['details']
            summonsHistory.resultReason = form.cleaned_data['resultReason']
            summonsHistory.date = datetime.now()
            summonsHistory.save()

            summons_obj.delete()

            request.session['standards_summons_msg'] = "Summons has been approved and archived succesfully."
        else:
            request.session['standards_summons_error'] = "Summons failed to be approved: " + str(form.errors)

        return redirect(manage_summons)
    else:
        return redirect(manage_summons)


@permission_required('Standards.delete_summons', login_url='pub-permission_denied')
def delete_summons(request, summons):
    """
        Reject a summons.
    """
    if request.method == 'POST':
        try:
            summons_obj = Summons.objects.get(pk=summons)
        except:
            request.session[
                'standards_summons_error'] = "Sorry, that summons no longer exists. It may have been approved or rejected already."
            return redirect(manage_summons)

        form = ArchiveSummonsForm(request.POST)

        if form.is_valid():
            summonsHistory = SummonsHistoryRecord()
            summonsHistory.summonee = summons_obj.summonee
            summonsHistory.summoner = summons_obj.summoner
            summonsHistory.saved_by = request.user
            summonsHistory.details = form.cleaned_data['details']
            summonsHistory.resultReason = form.cleaned_data['resultReason']
            summonsHistory.date = datetime.now()
            summonsHistory.rejected = True
            summonsHistory.save()
        else:
            request.session['standards_summons_error'] = "Summons failed to be rejected: " + str(form.errors)

        summons_obj.delete()
        request.session['standards_summons_msg'] = "Summons rejected successfully."

        return redirect(manage_summons)
    else:
        return redirect(manage_summons)
