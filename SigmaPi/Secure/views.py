from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from Secure.models import CalendarKey

@login_required
def index(request):
    """ View for the index landing page of the site """

    context = {
        'title': 'Sigma Pi - Secure',
        'secure_index': True,
        'calendar_url': get_special_url(request),
        'general_calendar_url': get_general_url()
    }

    return render(request, 'secure_home.html', context)

def get_special_url(request):
    groups = request.user.groups.exclude(name="Brothers")

    try:
        for group in groups:
            if len(CalendarKey.objects.filter(group=group)) > 0:
                cal_key = CalendarKey.objects.get(group=group)
                return "https://teamup.com/%s?view=l&sidepanel=c" % cal_key.key
    except:
        return False

def get_general_url():
    try:
        brothers = Group.objects.get(name="Brothers")
        cal_key = CalendarKey.objects.get(group=brothers)
        return "https://teamup.com/%s?view=d&sidepanel=c" % cal_key.key
    except:
        return False
