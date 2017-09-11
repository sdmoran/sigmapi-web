"""
API for Calendar invites.
"""
from django.conf import settings
from django.http import HttpResponse
from django.views import View


class SendInviteView(View):
    """
    TODO docstring
    """

    def post(request):
        """
        TODO docstring
        """
        key = request.content.get('key')
        if key != settings.CALENDAR_INVITE_API_KEY:
            return HttpResponse('Invalid API key.', status_code=401)
        invite_data = request.content.get('data')
        if not (invite_data and isinstance(invite_data, str)):
            return HttpResponse(
                '\'data\' parameter missing, empty, or not a string',
                status_code=422,
            )

        print('Received invite: ' + invite_data)  # TODO

        return HttpResponse(status_code=204)
