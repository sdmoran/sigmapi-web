"""
Utilites for Slack Apps
"""
import hashlib
import hmac
import time

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

SLACK_HTTP_TIMESTAMP = 'HTTP_X_SLACK_REQUEST_TIMESTAMP'
SLACK_HTTP_SIGNATURE = 'HTTP_X_SLACK_SIGNATURE'


def verify_slack_signature(func, client_secret):
    """
    Creates a decorator that can verify a request was actually sent from a specific slack app
    :param func: The function to wrap
    :param client_secret: The client secret for the slack app being verified as the source
    """

    def wrapper(request):
        """
        The wrapper function for this decorator
        """
        if SLACK_HTTP_TIMESTAMP in request.META and SLACK_HTTP_SIGNATURE in request.META:
            timestamp = request.META[SLACK_HTTP_TIMESTAMP]
            slack_signature = request.META[SLACK_HTTP_SIGNATURE]

            if abs(time.time() - int(timestamp)) > 60 * 5:
                # The request timestamp is more than five minutes from local time.
                # It could be a replay attack, so let's ignore it.
                return HttpResponse(status=400)

            sig_basestring = 'v0:' + str(timestamp) + ':' + request.body.decode('utf-8')

            my_signature = 'v0=' + hmac.new(
                client_secret,
                bytearray(sig_basestring, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            if hmac.compare_digest(my_signature, slack_signature):
                # hooray, the request came from Slack!
                return func(request)
            return HttpResponse('Slack signature verification failed', status=403)
        return HttpResponse('Slack command must include a signature', status=403)

    # Need to make the original func csrf exempt since we are using Slack's
    # signature verification method instead (not like we have a choice anyway)
    return csrf_exempt(wrapper)


def verify_sigma_poll_sig(func):
    """
    A decorator that verifies a message was sent from the Sigma Polls app
    :param func: The function to wrap
    """
    return verify_slack_signature(func, settings.SIGMA_POLLS_SLACK_CLIENT_SECRET)
