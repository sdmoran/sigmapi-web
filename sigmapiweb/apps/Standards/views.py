"""
Views for Standards app.
"""
from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from . import notify
from .forms import SummonsRequestForm, ArchiveSummonsForm
from .models import SummonsRequest, Summons, SummonsHistoryRecord


@login_required
def index(request):
    """
    Displays the homepage of the standards module.
    """
    summons_form = SummonsRequestForm()
    summons_history = SummonsHistoryRecord.objects.all().filter(
        summonee=request.user
    ).order_by('-date')

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

    return render(request, 'standards/index.html', context)


@permission_required(
    'Standards.add_summonsrequest',
    login_url='pub-permission_denied',
)
def send_summons_request(request):
    """
    View for sending a summons request.
    """
    # TODO: Refactor this to be able to remove this disable
    # pylint: disable=too-many-return-statements

    if request.method != 'POST':
        return redirect(index)

    num_recipients = int(request.POST['recipient-count'])

    # Check for reason
    spoke_with_str = request.POST.get('spokeWith', 'error')
    spoke_with = False
    if spoke_with_str == 'yes':
        spoke_with = True
    elif spoke_with_str != 'no':
        request.session['standards_index_error'] = (
            'Summons request failed to send. You must fill in all fields.'
        )
        return redirect(index)
    outcomes = request.POST.get('outcomes', '')
    standards_action = request.POST.get('standards_action', '')
    special_circumstance = request.POST.get('special_circumstance', '')

    if spoke_with:
        if not outcomes.strip():
            request.session['standards_index_error'] = (
                'Summons request failed to send. ' +
                'You must include outcomes of the conversation.'
            )
            return redirect(index)
        elif not standards_action.strip():
            request.session['standards_index_error'] = (
                'Summons request failed to send. ' +
                'You must include suggested further action by standards.'
            )
            return redirect(index)
    elif not special_circumstance.strip():
        request.session['standards_index_error'] = (
            'Summons request failed to send. ' +
            'You must include the special circumstance.'
        )
        return redirect(index)

    # Check for recipients
    num_summons_sent = 0
    for i in range(num_recipients):
        try:
            current_recipient = (
                request.POST['summonee_' + str(i + 1)]
                if i
                else request.POST['summonee']
            )
            if current_recipient.strip():
                recipient_int = int(current_recipient)
                recipient_user = User.objects.get(pk=recipient_int)
                summons_req = SummonsRequest(
                    summoner=request.user,
                    summonee=recipient_user,
                    spokeWith=spoke_with,
                    outcomes=outcomes,
                    standards_action=standards_action,
                    special_circumstance=special_circumstance,
                    dateRequestSent=datetime.now()
                )
                summons_req.save()
                num_summons_sent += 1
        except (KeyError, ValueError, User.DoesNotExist):
            request.session['standards_index_error'] = (
                'Unknown error occurred while processing summons recipient ' +
                'list. Please try again. If the problem persists, please ' +
                'contact the webmaster.'
            )
            return redirect(index)

    if num_summons_sent > 0:
        request.session['standards_index_msg'] = (
            'Summons request sent successfully!'
        )
        notify.summons_requested(num_summons_sent)
    else:
        request.session['standards_index_error'] = (
            'Summons request failed to send. ' +
            'You must include atleast 1 recipient with the request.'
        )
    return redirect(index)


@permission_required(
    'Standards.change_summonsrequest',
    login_url='pub-permission_denied',
)
def manage_summons_requests(request):
    """
    A view for managing summons requests and sending out summons.
    """
    current_requests = SummonsRequest.objects.all().order_by(
        '-dateRequestSent'
    )
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
    return render(request, 'standards/summons_requests.html', context)


@permission_required(
    'Standards.delete_summonsrequest',
    login_url='pub-permission_denied',
)
def reject_summons_request(request, summons_req):
    """
    A view for denying a summons request.
    """
    if request.method != 'POST':
        return redirect(manage_summons_requests)
    try:
        summons_request = SummonsRequest.objects.get(pk=summons_req)
    except SummonsRequest.DoesNotExist:
        request.session['standards_summons_error'] = (
            'Sorry, that summons request no longer exists. ' +
            'It may have been approved or rejected already.'
        )
        return redirect(manage_summons_requests)
    notify.summons_request_denied(summons_request)
    summons_request.delete()
    request.session['standards_summons_msg'] = (
        'Summons request successfully rejected.'
    )
    return redirect(manage_summons_requests)


@permission_required(
    'Standards.change_summonsrequest',
    login_url='pub-permission_denied',
)
def approve_summons_request(request, summons_req):
    """
    View for approving a summons request.
    """
    if request.method != 'POST':
        return redirect(manage_summons_requests)
    try:
        summons_request = SummonsRequest.objects.get(pk=summons_req)
    except SummonsRequest.DoesNotExist:
        request.session['standards_summons_error'] = (
            'Sorry, that summons request no longer exists. ' +
            'It may have been approved or rejected already.'
        )
        return redirect(manage_summons_requests)

    approved_summons = Summons(
        summoner=summons_request.summoner,
        summonee=summons_request.summonee,
        approver=request.user,
        spokeWith=summons_request.spokeWith,
        outcomes=summons_request.outcomes,
        standards_action=summons_request.standards_action,
        special_circumstance=summons_request.special_circumstance,
        dateSummonsSent=datetime.now()
    )
    approved_summons.save()
    summons_request.delete()

    notify.summons_sent(approved_summons)

    request.session['standards_summons_msg'] = (
        'Summons request successfully accepted.'
    )
    return redirect(manage_summons_requests)


@permission_required(
    'Standards.change_summons',
    login_url='pub-permission_denied'
)
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

    return render(request, 'standards/summons.html', context)


@permission_required(
    'Standards.change_summons',
    login_url='pub-permission_denied'
)
def accept_summons(request, summons):
    """
    Accept a summons and turn it into a SummonsHistoryRecord object.
    """
    if request.method != 'POST':
        return redirect(manage_summons)
    try:
        summons_obj = Summons.objects.get(pk=summons)
    except SummonsRequest.DoesNotExist:
        request.session['standards_summons_error'] = (
            'Sorry, that summons no longer exists. ' +
            'It may have been approved or rejected already.'
        )
        return redirect(manage_summons)

    form = ArchiveSummonsForm(request.POST)

    if form.is_valid():

        summons_history = SummonsHistoryRecord(
            summonee=summons_obj.summonee,
            summoner=summons_obj.summoner,
            saved_by=request.user,
            details=form.cleaned_data['details'],
            resultReason=form.cleaned_data['resultReason'],
            date=datetime.now(),
        )
        summons_history.save()

        summons_obj.delete()

        request.session['standards_summons_msg'] = (
            'Summons has been approved and archived succesfully.'
        )
    else:
        request.session['standards_summons_error'] = (
            'Summons failed to be approved: ' + str(form.errors)
        )
    return redirect(manage_summons)


@permission_required(
    'Standards.delete_summons',
    login_url='pub-permission_denied',
)
def delete_summons(request, summons):
    """
    Reject a summons.
    """
    if request.method != 'POST':
        return redirect(manage_summons)
    try:
        summons_obj = Summons.objects.get(pk=summons)
    except Summons.DoesNotExist:
        request.session[
            'standards_summons_error'] = (
                'Sorry, that summons no longer exists. ' +
                'It may have been approved or rejected already.'
            )
        return redirect(manage_summons)

    form = ArchiveSummonsForm(request.POST)

    if form.is_valid():
        summons_history = SummonsHistoryRecord(
            summonee=summons_obj.summonee,
            summoner=summons_obj.summoner,
            saved_by=request.user,
            details=form.cleaned_data['details'],
            resultReason=form.cleaned_data['resultReason'],
            date=datetime.now(),
            rejected=True,
        )
        summons_history.save()
    else:
        request.session['standards_summons_error'] = (
            'Summons failed to be rejected: ' + str(form.errors)
        )

    summons_obj.delete()
    request.session['standards_summons_msg'] = (
        'Summons rejected successfully.'
    )
    return redirect(manage_summons)
